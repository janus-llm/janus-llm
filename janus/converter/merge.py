import json
from collections import defaultdict

from langchain_core.runnables import Runnable, RunnableParallel

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.parsers.code_parser import IncompleteCodeParser
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
        for block in blocks:
            if block.block_label not in self._input_labels:
                continue

            block_hash = hash(block)
            hash_table[block_hash] = block

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
            descendents.intersection_update(hash_table)

            # Check that all input labels are represented
            labels_present = set(hash_table[h].block_label for h in descendents)
            if labels_present != self._input_labels:
                continue

            # Remove descendents from the hash table, add them to this group
            groups.append((ancestor, [hash_table.pop(d) for d in descendents]))

        if hash_table:
            raise ValueError(f"Found {len(hash_table)} blocks with no matches in merge")

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


class OutputMergerTranslator(Converter):
    """A class that translates outputs from the OutputMerger to code."""

    def __init__(
        self,
        input_labels: set[str]
        | str
        | None = None,  # this should be the output label of the OutputMerger
        target_language: str = "python",
        **kwargs,
    ) -> None:
        super().__init__(
            input_labels=input_labels,
            target_language=target_language,
            **kwargs,
        )
        self._label_dict = defaultdict(list)
        self._parser = IncompleteCodeParser(language=self._target_language)

    def _get_label_context(self, label):
        return lambda x: self._label_dict[label]

    def _get_context(self, block: CodeBlock) -> None:
        print(block.text)
        self._label_dict = json.loads(block.text)
        self._label_dict["TARGET_LANGUAGE"] = self._target_language

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            {label: self._get_label_context(label) for label in self._label_dict.keys()}
        )

    def _translate_block(self, block: CodeBlock) -> TranslatedCodeBlock | CodeBlock:
        if self._input_types is not None and block.block_type not in self._input_types:
            return block

        if self._input_labels is not None and block.block_label not in self._input_labels:
            return block

        self._get_context(block)
        return self._iterative_translate(block)
