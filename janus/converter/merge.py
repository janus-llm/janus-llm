import json
from collections import defaultdict

from langchain_core.runnables import Runnable, RunnableLambda

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.utils.logger import create_logger

log = create_logger(__name__)


class OutputMerger(Converter):
    def __init__(
        self,
        input_labels: set[str] | str | None = None,
        label_key_map: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        if input_labels is None:
            raise ValueError("OutputMerger requires input label list, recieved None")

        self._input_labels: set[str]
        super().__init__(
            input_labels=input_labels,
            **kwargs,
        )
        # self._input_labels = set(sorted(self._input_labels))
        if label_key_map is None:
            label_key_map = {k: k for k in sorted(self._input_labels)}
        self._label_key_map = label_key_map

    def _translate_blocks(
        self,
        blocks: list[CodeBlock],
    ) -> list[TranslatedCodeBlock | CodeBlock]:
        hash_table: dict[int, CodeBlock] = {}
        descendent_dict: dict[int, set[int]] = defaultdict(set)
        groupless_blocks: set[int] = set()
        for block in blocks:
            block_hash = hash(block)
            hash_table[block_hash] = block

            if block.block_label not in self._input_labels:
                continue

            groupless_blocks.add(block_hash)

            # If block has no history, it may be the original source
            if block.previous_generation is None:
                descendent_dict[block_hash].add(block_hash)
                continue

            prev_gen = block.previous_generation
            while not isinstance(prev_gen, str):
                descendent_dict[prev_gen["metadata"]["hash"]].add(block_hash)
                prev_gen = prev_gen["input"]

        ancestor_keys = sorted(descendent_dict, key=lambda k: len(descendent_dict[k]))
        ancestors: list[CodeBlock] = [hash_table[k] for k in ancestor_keys]

        # Work from smallest to largest group of "families", as a heuristic for
        #  searching from last common ancestor to first
        groups: list[tuple[CodeBlock, list[CodeBlock]]] = []
        for ancestor, key in zip(ancestors, ancestor_keys):
            descendents = descendent_dict[key]

            # Discard descendents that have already been taken
            descendents.intersection_update(groupless_blocks)

            # Check that all input labels are represented
            labels_present = set(hash_table[h].block_label for h in descendents)
            if labels_present != self._input_labels:
                continue

            # Remove descendents from the hash table, add them to this group
            groups.append((ancestor, [hash_table[d] for d in descendents]))
            groupless_blocks.difference_update(descendents)

        if groupless_blocks:
            raise ValueError(
                f"Found {len(groupless_blocks)} blocks with no matches in merge"
            )

        merged_blocks = [
            self._merge_group(group=descendents, ancestor=ancestor)
            for ancestor, descendents in groups
        ]

        return blocks + merged_blocks

    def _merge_group(
        self, group: list[CodeBlock], ancestor: CodeBlock
    ) -> TranslatedCodeBlock:
        if len(lengths := set(len(block.children) for block in group)) > 1:
            raise ValueError("Blocks have different numbers of children")
        [n_children] = lengths
        if len(ancestor.children) != n_children:
            raise ValueError("Group's common ancestor does not match number of children")

        translated_block = TranslatedCodeBlock(
            original=None,
            language="json",
            converter=self,
            model_name=None,
            block_type=self._output_type,
            block_label=self._output_label,
        )
        translated_block.previous_generation = ancestor.to_janus_object()
        translated_block.translated = True

        # If this is not a leaf node, recurse
        if n_children > 0:
            child_groups: list[list[CodeBlock]] = list(
                map(list, zip(*[block.children for block in group]))
            )
            for child_anc, child_group in zip(ancestor.children, child_groups):
                child = self._merge_group(group=child_group, ancestor=child_anc)
                translated_block.children.append(child)
            return translated_block

        # Collect the group's texts into a json
        label_dict: dict[str, list[str]] = defaultdict(list)
        for block in group:
            if block.text is None:
                continue
            if block.block_label not in self._label_key_map:
                raise ValueError(f"Unexpected block label: {block.block_label}")
            output_label = self._label_key_map[block.block_label]
            label_dict[output_label].append(block.text)

        translated_block.text = json.dumps(
            {key: "\n\n".join(value) for key, value in label_dict.items()}
        )

        return translated_block


class MergedOutputConverterMixin:
    """A mix-in that enables a Converter to use the result of OutputMerger as its input"""

    def _load_prompt(self) -> None:
        super()._load_prompt()
        self._expected_labels = set(self._prompt.input_variables)

    def _check_label_presence(self, block: CodeBlock) -> None:
        if block.text is None:
            return

        input_labels = set(json.loads(block.text).keys())
        if not self._expected_labels.issuperset(input_labels):
            raise ValueError(
                f"Input labels ({input_labels}) not captured in prompt"
                f" labels ({self._expected_labels}). Your prompt may need to be updated"
                " for the merged fields coming in."
            )

    def _input_runnable(self) -> Runnable:
        block_to_dict = RunnableLambda(lambda block: json.loads(block.text))
        return block_to_dict.assign(
            context=self._retriever,
        )

    def _translate_block(self, block: CodeBlock) -> TranslatedCodeBlock | CodeBlock:
        self._load_parameters()

        if self._input_types is not None and block.block_type not in self._input_types:
            return block

        if self._input_labels is not None and block.block_label not in self._input_labels:
            return block

        self._check_label_presence(block)
        return self._iterative_translate(block)
