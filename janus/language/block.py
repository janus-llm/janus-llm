import json
from functools import total_ordering
from typing import (
    TYPE_CHECKING,
    ForwardRef,
    Hashable,
    NotRequired,
    Optional,
    Tuple,
    TypedDict,
)

from janus.language.node import NodeType
from janus.utils.logger import create_logger

if TYPE_CHECKING:
    from janus.converter.converter import Converter

log = create_logger(__name__)


class JanusMetadata(TypedDict):
    cost: float
    processing_time: float
    num_requests: int
    input_tokens: int
    output_tokens: int
    converter_name: str
    language: str
    model_name: str
    type: str | None
    label: str | None


class JanusOutputObject(TypedDict):
    input: str
    metadata: JanusMetadata
    outputs: list["JanusOutputObject"] | list[str]
    intermediate_outputs: NotRequired[list["JanusOutputObject"]]


def combine_metadata(metadatas: list[JanusMetadata]) -> JanusMetadata:
    def _sum_metadata(key: str) -> float:
        return sum((m[key] for m in metadatas), start=0.0)

    def _concat_metadata(key: str) -> str:
        if len(set(m[key] for m in metadatas)) == 1:
            return metadatas[0][key]
        lst = ", ".join(str(m[key]) for m in metadatas)
        return f"[{lst}]"

    return {
        "cost": _sum_metadata("cost"),
        "processing_time": _sum_metadata("processing_time"),
        "num_requests": int(_sum_metadata("num_requests")),
        "input_tokens": int(_sum_metadata("input_tokens")),
        "output_tokens": int(_sum_metadata("output_tokens")),
        "converter_name": _concat_metadata("converter_name"),
        "model_name": _concat_metadata("model_name"),
        "language": _concat_metadata("language"),
        "type": _concat_metadata("type"),
        "label": _concat_metadata("label"),
    }


@total_ordering
class CodeBlock:
    """A class that represents a functional block of code.

    Attributes:
        id: The id of the code block in the AST
        name: Descriptive name of node
        node_type: The type of the code block ('function', 'module', etc.). Defined in the
            language-specific modules.
        language: The language of the code block.
        text: The code block.
        start_point: The line and column numbers of the first line of the code block.
        end_point: The line and column numbers of the last line of the code block.
        start_byte: starting byte offset into file
        end_byte: ending byte offset into file
        tokens: The number of tokens in the code block.
        children: A tuple of child code blocks.
        embedding_id: id of embedding
        affixes: prefix and suffix text for node
        complete: Rolls up self and children's complete status, incomplete means a child
            is missing.
    """

    def __init__(
        self,
        id: Hashable,
        name: Optional[str],
        node_type: NodeType,
        language: str,
        text: Optional[str],
        start_point: Optional[Tuple[int, int]],
        end_point: Optional[Tuple[int, int]],
        start_byte: Optional[int],
        end_byte: Optional[int],
        tokens: int,
        children: list["CodeBlock"],
        embedding_id: Optional[str] = None,
        affixes: Tuple[str, str] = ("", ""),
        context_tags: dict[str, str] = {},
        previous_generations: list[JanusOutputObject] = [],
        block_type: str | None = None,
        block_label: str | None = None,
    ) -> None:
        self.id: Hashable = id
        self.name: Optional[str] = name
        self.node_type: NodeType = node_type
        self.language: str = language
        self.text: Optional[str] = text
        self.start_point: Optional[Tuple[int, int]] = start_point
        self.end_point: Optional[Tuple[int, int]] = end_point
        self.start_byte: Optional[int] = start_byte
        self.end_byte: Optional[int] = end_byte
        self.tokens: int = tokens
        self.children: list["CodeBlock"] = sorted(children)
        self.embedding_id: Optional[str] = embedding_id
        self.affixes: Tuple[str, str] = affixes
        self.context_tags: dict[str, str] = context_tags

        self.complete = True
        self.omit_prefix = True
        self.omit_suffix = False
        self.previous_generations = previous_generations
        self.block_type = block_type
        self.block_label = block_label

        if self.children:
            self.children[0].omit_prefix = False

    def __lt__(self, other: "CodeBlock") -> bool:
        return (self.start_byte, self.end_byte) < (other.start_byte, other.end_byte)

    def __eq__(self, other: "CodeBlock") -> bool:
        return (self.start_byte, self.end_byte) == (other.start_byte, other.end_byte)

    @property
    def prefix(self) -> str:
        return self.affixes[0] if not self.omit_prefix else ""

    @property
    def suffix(self) -> str:
        return self.affixes[1] if not self.omit_suffix else ""

    @property
    def complete_text(self) -> str:
        return f"{self.prefix}{self.text or ''}{self.suffix}"

    @property
    def n_descendents(self) -> int:
        """The total number of descendents of this block

        Returns:
            The total number of descendents of this block
        """
        return 1 + sum(c.n_descendents for c in self.children)

    @property
    def height(self) -> int:
        """The number of edges between this node and a leaf

        Returns:
            The number of edges between this node and a leaf
        """
        return 1 + max(c.height for c in self.children) if self.children else 0

    @property
    def max_tokens(self) -> int:
        """The maximum number of tokens in this block or any of its descendents

        Returns:
            The maximum number of tokens in this block or any of  its descendents
        """
        return max([self.tokens, *[c.max_tokens for c in self.children]])

    @property
    def total_tokens(self) -> int:
        """The total tokens represented by this block and all its descendents

        Returns:
            The total number of tokens represented by this block and all its
            descendents
        """
        return self.tokens + sum(c.total_tokens for c in self.children)

    def pop_prefix(self) -> str:
        """Get this block's prefix and remove it from the block. This may be used
        to transfer the prefix from the first child of a node to its parent.
        """
        prefix = self.affixes[0]
        self.affixes = ("", self.affixes[1])
        return prefix

    def pop_suffix(self) -> str:
        """Get this block's suffix and remove it from the block. This may be used
        to transfer the suffix from the first child of a node to its parent.
        """
        suffix = self.affixes[1]
        self.affixes = (self.affixes[0], "")
        return suffix

    def rebuild_text_from_children(self):
        if self.children:
            prefix = self.affixes[0] + self.children[0].pop_prefix()
            suffix = self.children[-1].pop_suffix() + self.affixes[1]
            self.text = "".join(c.complete_text for c in self.children)
            self.affixes = (prefix, suffix)
            self.tokens = sum(c.tokens for c in self.children)

    def tree_str(self, depth: int = 0) -> str:
        """A string representation of the tree with this block as the root

        Returns:
            A string representation of the tree with this block as the root
        """
        tokens = self.tokens
        identifier = str(self.id)
        if self.text is None:
            identifier = f"({identifier})"
            tokens = self.total_tokens
        elif not self.complete:
            identifier += "*"
        if self.start_point is not None and self.end_point is not None:
            start = f"{self.start_point[0]}:{self.start_point[1]}"
            end = f"{self.end_point[0]}:{self.end_point[1]}"
            seg = f" [{start}-{end}]"
        else:
            seg = ""
        return "\n".join(
            [
                f"{'| '*depth}{identifier}{seg}  ({tokens:,d} tokens)",
                *[c.tree_str(depth + 1) for c in self.children],
            ]
        )

    @classmethod
    def extract_from_janus_object(cls, janus_obj: JanusOutputObject) -> "CodeBlock":
        source_language = "UNKNOWN"
        previous_generations: list[JanusOutputObject] = janus_obj["intermediate_outputs"]
        if previous_generations:
            source_language = previous_generations[-1]["metadata"]["language"]

        input = janus_obj["input"]
        input_lines = input.split("\n")
        end_line = len(input_lines) - 1
        end_char = len(input_lines[-1]) - 1
        end_byte = len(bytes(input, "utf-8")) - 1

        # Create a TranslatedCodeBlock using the input text and metadata
        return CodeBlock(
            id="dummy",
            name="dummy",
            node_type=NodeType("dummy"),
            language=source_language,
            text=input,
            start_point=(0, 0),
            end_point=(end_line, end_char),
            start_byte=0,
            end_byte=end_byte,
            tokens=0,
            children=[],
            previous_generations=previous_generations,
        )


class TranslatedCodeBlock(CodeBlock):
    """A class that represents the translated functional block of code.

    Attributes:
        original: The original code block.
        cost: The total cost to translate the original code block.
        translated: Whether this block has been successfully translated
    """

    def __init__(
        self,
        original: CodeBlock,
        language: str,
        converter: str | ForwardRef("Converter"),
        model_name: str | None = None,
        block_type: str | None = None,
        block_label: str | None = None,
    ) -> None:
        """Create an "empty" `TranslatedCodeBlock` from the given original

        Arguments:
            original: The original code block
            language: The language to translate to
            converter: the converter used to translate
            block_type: type of the block
            block_label: label for block
            (for mapping outputs to inputs through ConverterChain)

        Returns:
            A `TranslatedCodeBlock` with the same attributes as the original, except
            for `text`, `path`, `complete`, `language`, `tokens`, and `children`
        """
        self.children: list[TranslatedCodeBlock]
        super().__init__(
            id=original.id,
            name=original.name,
            node_type=original.node_type,
            language=language,
            text=None,
            start_point=original.start_point,
            end_point=original.end_point,
            start_byte=None,
            end_byte=None,
            tokens=0,
            children=[
                TranslatedCodeBlock(child, language, converter, block_type, block_label)
                for child in original.children
            ],
            affixes=original.affixes,
            previous_generations=original.previous_generations,
            block_type=block_type,
            block_label=block_label,
        )

        self.original = original
        self.converter = converter

        self.model_name: str = model_name or "UNKNOWN"
        if not isinstance(converter, str):
            self.model_name = converter._model_name

        self.complete = original.complete
        self.translated = False
        self.cost = 0
        self.num_requests = 0
        self.tokens = 0
        self.processing_time = 0

        self.request_input_tokens = 0
        self.request_output_tokens = 0

    @property
    def total_cost(self) -> float:
        """The total cost spent translating this block and all its descendents

        Returns:
            The total cost spent translating this block and all its descendents
        """
        return self.cost + sum(c.total_cost for c in self.children)

    @property
    def total_input_tokens(self) -> int:
        """The total number of input tokens represented by this block and all its
        successfully-translated descendents

        Returns:
            The total number of input tokens represented by this block and all its
        """
        children_sum = sum(c.total_input_tokens for c in self.children)
        return children_sum + (self.original.tokens if self.translated else 0)

    @property
    def total_request_input_tokens(self) -> int:
        """
        The total number of tokens sent to LLM during all requests during translation

        Returns:
            The total number of tokens sent to LLM during all requests during translation
        """
        children_sum = sum(c.total_request_input_tokens for c in self.children)
        return children_sum + self.request_input_tokens

    @property
    def total_request_output_tokens(self) -> int:
        """
        The total number of tokens output by an LLM during translation

        Returns:
            The total number of tokens output by an LLM during translation
        """
        children_sum = sum(c.total_request_output_tokens for c in self.children)
        return children_sum + self.request_output_tokens

    @property
    def total_num_requests(self) -> int:
        """
        Total number of requests made to LLM during translation

        Returns:
            Total number of requests made to LLM during translation
        """
        children_sum = sum(c.total_num_requests for c in self.children)
        return children_sum + self.num_requests

    @property
    def total_processing_time(self) -> float:
        children_sum = sum(c.total_processing_time for c in self.children)
        return children_sum + self.processing_time

    @property
    def translation_completed(self) -> bool:
        """Whether or not the code block was successfully translated

        Returns:
            Whether or not the code block was successfully translated
        """
        return self.translated and all(c.translation_completed for c in self.children)

    @property
    def translation_completeness(self) -> float:
        """The share of the input that was successfully translated

        Returns:
            The share of the input that was successfully translated
        """
        return (
            (self.total_input_tokens / self.original.total_tokens)
            if self.original.total_tokens
            else 0
        )

    def to_janus_object(self, combine_children: bool = True) -> JanusOutputObject:
        metadata: JanusMetadata = {
            "cost": self.total_cost,
            "processing_time": self.total_processing_time,
            "num_requests": self.total_num_requests,
            "input_tokens": self.total_request_input_tokens,
            "output_tokens": self.total_request_output_tokens,
            "converter_name": self.converter.__class__.__name__,
            "language": self.language,
            "model_name": self.model_name,
            "type": self.block_type,
            "label": self.block_label,
        }
        if combine_children:
            outputs = [self.complete_text]
        else:
            outputs = self.descendant_janus_objects()
        obj: JanusOutputObject = {
            "input": self.original.complete_text,
            "metadata": metadata,
            "outputs": outputs,
            "intermediate_outputs": self.previous_generations,
        }
        return obj

    def descendant_janus_objects(self) -> list[JanusOutputObject]:
        if not self.children:
            return [self.to_janus_object()]
        return [obj for c in self.children for obj in c.descendant_janus_objects()]

    @classmethod
    def from_janus_object(
        cls,
        janus_obj: JanusOutputObject,
    ) -> "TranslatedCodeBlock":
        metadata = janus_obj["metadata"]

        code_block = CodeBlock.extract_from_janus_object(janus_obj)
        translated_block = TranslatedCodeBlock(
            original=code_block,
            language=metadata["language"],
            converter=metadata["converter_name"],
            model_name=metadata["model_name"],
            block_type=janus_obj["type"],
            block_label=janus_obj["label"],
        )
        translated_block.text = json.dumps(janus_obj["outputs"])
        translated_block.cost = metadata["cost"]
        translated_block.processing_time = metadata["processing_time"]
        translated_block.num_requests = metadata["num_requests"]
        translated_block.request_input_tokens = metadata["input_tokens"]
        translated_block.request_output_tokens = metadata["output_tokens"]
        return translated_block

    def to_codeblock(self) -> CodeBlock:
        prev_gen = self.previous_generations + [self.to_janus_object()]
        return CodeBlock(
            id=self.id,
            name=self.name,
            node_type=self.node_type,
            language=self.language,
            text=self.text,
            start_point=self.start_point,
            end_point=self.end_point,
            start_byte=self.start_byte,
            end_byte=self.end_byte,
            embedding_id=self.embedding_id,
            tokens=self.tokens,
            children=[child.to_codeblock() for child in self.children],
            affixes=self.affixes,
            previous_generations=prev_gen,
            block_type=self.block_type,
            block_label=self.block_label,
        )

    def __iadd__(self, other):
        self.cost += other.cost
        self.num_requests += other.num_requests
        self.processing_time += other.processing_time
        self.request_input_tokens += other.request_input_tokens
        self.request_output_tokens += other.request_output_tokens
        return self


class BlockCollection:
    def __init__(
        self,
        blocks: list[CodeBlock],
        previous_generations: list["TranslatedBlockCollection"] = [],
    ):
        self.blocks = blocks
        self.previous_generations = previous_generations


class TranslatedBlockCollection:
    def __init__(
        self,
        blocks: list[TranslatedCodeBlock],
        previous_generations: list["TranslatedBlockCollection"] = [],
    ):
        self.blocks = blocks
        self.previous_generations = previous_generations

    def to_block_collection(self) -> "BlockCollection":
        return BlockCollection(
            blocks=[b.to_codeblock() for b in self.blocks],
            previous_generations=self.previous_generations + [self],
        )

    @classmethod
    def from_janus_object(
        cls, janus_obj: JanusOutputObject
    ) -> "TranslatedBlockCollection":
        metadata: JanusMetadata = janus_obj["metadata"]
        previous_generations: list[JanusOutputObject] = janus_obj["intermediate_outputs"]

        previous_generation_blocks: list[TranslatedBlockCollection] = list(
            map(
                cls.from_janus_object,
                previous_generations,
            )
        )

        code_block = CodeBlock.extract_from_janus_object(janus_obj)

        results: list[TranslatedCodeBlock] = []
        for i, out_obj in enumerate(janus_obj["outputs"]):
            if not isinstance(out_obj, str):
                # If the output is a janus output object, recurse
                results.extend(cls.from_janus_object(out_obj).blocks)
                continue

            # Create a TranslatedCodeBlock using the input text and metadata
            translated_block = TranslatedCodeBlock(
                original=code_block,
                language=metadata["language"],
                converter=metadata["converter_name"],
                model_name=metadata["model_name"],
                block_type=metadata["type"],
                block_label=metadata["label"],
            )
            # Copy over the output text and the rest of the metadata
            translated_block.text = out_obj
            translated_block.cost = metadata["cost"]
            translated_block.processing_time = metadata["processing_time"]
            translated_block.num_requests = metadata["num_requests"]
            translated_block.request_input_tokens = metadata["input_tokens"]
            translated_block.request_output_tokens = metadata["output_tokens"]
            results.append(translated_block)

        return TranslatedBlockCollection(results, previous_generation_blocks)

    def to_janus_object(self, combine_children: bool = True) -> JanusOutputObject:
        input = json.dumps([block.original.complete_text for block in self.blocks])
        outputs = [block.to_janus_object(combine_children) for block in self.blocks]
        metadata = combine_metadata([obj["metadata"] for obj in outputs])
        prev_gens = [c.to_janus_object() for c in self.previous_generations]

        out: JanusOutputObject = {
            "input": input,
            "metadata": metadata,
            "outputs": outputs,
            "intermediate_outputs": prev_gens,
        }

        return out

    @property
    def total_cost(self):
        return sum(b.total_cost for b in self.blocks)

    @property
    def total_processing_time(self):
        return sum(b.total_processing_time for b in self.blocks)

    @property
    def total_request_input_tokens(self):
        return sum(b.total_request_input_tokens for b in self.blocks)

    @property
    def total_request_output_tokens(self):
        return sum(b.total_request_output_tokens for b in self.blocks)

    @property
    def total_num_requests(self):
        return sum(b.total_num_requests for b in self.blocks)

    @property
    def block_type(self):
        return None

    @property
    def block_label(self):
        return None

    @property
    def translation_completed(self):
        return all(b.translation_completed for b in self.blocks)

    @property
    def complete(self):
        return all(b.complete for b in self.blocks)
