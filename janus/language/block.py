import random
from collections import OrderedDict
from copy import deepcopy
from functools import total_ordering
from typing import (
    TYPE_CHECKING,
    ForwardRef,
    Hashable,
    Iterable,
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
RNG = random.Random()


class JanusMetadata(TypedDict):
    cost: NotRequired[float]
    processing_time: NotRequired[float]
    num_requests: NotRequired[int]
    request_input_tokens: NotRequired[int]
    request_output_tokens: NotRequired[int]
    input_tokens: NotRequired[int]
    output_tokens: int
    start_line: int
    start_char: int
    start_byte: int
    end_line: int
    end_char: int
    end_byte: int
    converter_name: NotRequired[str]
    language: str
    model_name: NotRequired[str]
    type: NotRequired[str]
    label: NotRequired[str]
    translation_complete: bool


class JanusOutputObject(TypedDict):
    input: str | ForwardRef("JanusOutputObject")
    metadata: JanusMetadata
    output: NotRequired[str]
    outputs: list["JanusOutputObject"]


def sort_janus_obj(obj: JanusOutputObject) -> OrderedDict:
    metadata_key_order = [
        "converter_name",
        "translation_complete",
        "language",
        "model_name",
        "type",
        "label",
        "cost",
        "processing_time",
        "request_input_tokens",
        "request_output_tokens",
        "num_requests",
        "input_tokens",
        "output_tokens",
        "start_line",
        "start_char",
        "start_byte",
        "end_line",
        "end_char",
        "end_byte",
    ]
    ordered_metadata = OrderedDict()
    for k in metadata_key_order:
        if k in obj["metadata"]:
            ordered_metadata[k] = obj["metadata"][k]

    ordered_obj = OrderedDict()
    ordered_obj["metadata"] = ordered_metadata
    if "output" in obj:
        ordered_obj["output"] = obj["output"]
    ordered_obj["outputs"] = [sort_janus_obj(o) for o in obj["outputs"]]
    if isinstance(obj["input"], dict):
        ordered_obj["input"] = sort_janus_obj(obj["input"])
    else:
        ordered_obj["input"] = obj["input"]

    return ordered_obj


def combine_metadata(metadatas: Iterable[JanusMetadata]) -> JanusMetadata:
    metadatas = list(metadatas)
    if not metadatas:
        return JanusMetadata(
            output_tokens=0,
            start_line=0,
            start_char=0,
            start_byte=0,
            end_line=-1,
            end_char=-1,
            end_byte=-1,
            language="",
            translation_complete=False,
        )

    def _get_vals(key: str) -> list:
        return [m[key] for m in metadatas if key in m]

    def _sum_metadata(key: str) -> float | None:
        if not (vals := _get_vals(key)):
            return None
        return sum(vals, start=0.0)

    def _min_metadata(key: str) -> float | None:
        if not (vals := _get_vals(key)):
            return None
        return min(vals)

    def _max_metadata(key: str) -> float | None:
        if not (vals := _get_vals(key)):
            return None
        return max(vals)

    def _merge_metadata(key: str) -> str | None:
        if len(vals := _get_vals(key)) != len(metadatas):
            return None

        if len(set(vals)) == 1:
            return vals[0]

        return None
        lst = ", ".join(map(str, vals))
        return f"[{lst}]"

    def _all_metadata(key: str) -> bool | None:
        if not (vals := _get_vals(key)):
            return None
        return all(vals)

    first_line_idx = min(range(len(metadatas)), key=lambda i: metadatas[i]["start_line"])
    last_line_idx = max(range(len(metadatas)), key=lambda i: metadatas[i]["end_line"])

    metadata: JanusMetadata = {
        "output_tokens": int(_sum_metadata("output_tokens") or 0),
        "start_line": metadatas[first_line_idx]["start_line"],
        "start_char": metadatas[first_line_idx]["start_char"],
        "start_byte": int(_min_metadata("start_byte") or 0),
        "end_line": metadatas[last_line_idx]["end_line"],
        "end_char": metadatas[last_line_idx]["end_char"],
        "end_byte": int(_max_metadata("end_byte") or -1),
        "language": _merge_metadata("language") or "UNKNOWN",
        "translation_complete": _all_metadata("translation_complete") or False,
    }

    optional_metadata = {
        "cost": _sum_metadata("cost") or 0.0,
        "processing_time": _sum_metadata("processing_time") or 0.0,
        "num_requests": int(_sum_metadata("num_requests") or 0),
        "request_input_tokens": int(_sum_metadata("request_input_tokens") or 0),
        "request_output_tokens": int(_sum_metadata("request_output_tokens") or 0),
        "input_tokens": int(_sum_metadata("input_tokens") or 0),
        "converter_name": _merge_metadata("converter_name") or None,
        "model_name": _merge_metadata("model_name") or None,
        "type": _merge_metadata("type") or None,
        "label": _merge_metadata("label") or None,
    }

    for k, v in optional_metadata.items():
        if v is not None:
            metadata[k] = v

    return metadata


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
        children: list["CodeBlock"] | None = None,
        start_point: Tuple[int, int] = (0, 0),
        end_point: Tuple[int, int] = (-1, -1),
        start_byte: int = 0,
        end_byte: int = -1,
        tokens: int = 0,
        embedding_id: Optional[str] = None,
        affixes: Tuple[str, str] = ("", ""),
        context_tags: dict[str, str] = {},
        previous_generation: JanusOutputObject | None = None,
        block_type: str | None = None,
        block_label: str | None = None,
    ) -> None:
        self.id: Hashable = id
        self.name: Optional[str] = name
        self.node_type: NodeType = node_type
        self.language: str = language
        self.text: Optional[str] = text
        self.start_point: tuple[int, int] = start_point
        self.end_point: tuple[int, int] = end_point
        self.start_byte: int = start_byte
        self.end_byte: int = end_byte
        self.tokens: int = tokens
        self.embedding_id: Optional[str] = embedding_id
        self.affixes: Tuple[str, str] = affixes
        self.context_tags: dict[str, str] = context_tags

        self.complete = True
        self.omit_prefix = True
        self.omit_suffix = False
        self.previous_generation = previous_generation
        self.block_type = block_type
        self.block_label = block_label

        self.children: list["CodeBlock"] = []
        if children is not None:
            self.set_children(children)

    @classmethod
    def get_empty(cls) -> "CodeBlock":
        return CodeBlock(
            id="NULL",
            name="NULL",
            node_type=NodeType("NULL"),
            language="UNKNOWN",
            text=None,
            children=[],
        )

    def __lt__(self, other: "CodeBlock") -> bool:
        return (self.start_byte, self.end_byte) < (other.start_byte, other.end_byte)

    def __eq__(self, other: "CodeBlock") -> bool:
        return (self.start_byte, self.end_byte) == (other.start_byte, other.end_byte)

    def __hash__(self) -> int:
        if self.previous_generation is not None:
            return hash((self.text, hash(self.previous_generation["output"])))
        return hash(self.text)

    def set_children(self, children: list["CodeBlock"]) -> None:
        self.children = children
        self.sort_children()

    def sort_children(self) -> None:
        self.children = sorted(self.children)
        for child in self.children:
            child.omit_prefix = True
            child.omit_suffix = False
            child.sort_children()
        if self.children:
            self.children[0].mark_first()
            self.children[-1].mark_last()

    def mark_first(self) -> None:
        self.omit_prefix = False
        if self.children:
            self.children[0].mark_first()

    def mark_last(self) -> None:
        self.omit_suffix = False
        if self.children:
            self.children[-1].mark_last()

    def mark_root(self) -> None:
        self.mark_first()
        self.mark_last()
        self.set_start_index(0, 0, 0)

    def set_start_index(self, byte: int, line: int, char: int) -> None:
        self.start_byte = byte
        self.start_point = (line, char)

        def _increment_indices(text: str):
            nonlocal byte, line, char
            byte += len(bytes(text, "utf-8"))
            newlines = text.count("\n")
            if newlines:
                char = len(text.rsplit("\n", 1)[1])
            else:
                char += len(text)
            line += newlines

        _increment_indices(self.prefix)

        if self.text is not None:
            _increment_indices(self.text)

        for child in self.children:
            child.set_start_index(byte=byte, line=line, char=char)
            byte = child.end_byte
            line, char = child.end_point

        _increment_indices(self.suffix)

        self.end_byte = byte
        self.end_point = (line, char)

    @property
    def prefix(self) -> str:
        return self.affixes[0] if not self.omit_prefix else ""

    @property
    def suffix(self) -> str:
        return self.affixes[1] if not self.omit_suffix else ""

    @property
    def complete_text(self) -> str:
        text = self.text
        if text is None and self.children:
            text = "".join(c.complete_text for c in self.children)
        return f"{self.prefix}{text or ''}{self.suffix}"

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
            for child in self.children:
                child.rebuild_text_from_children()
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
    def extract_input(cls, janus_obj: JanusOutputObject) -> "CodeBlock":
        """Get the CodeBlock corresponding to the input of the given JanusOutputObject"""
        if isinstance(janus_obj["input"], dict):
            return TranslatedCodeBlock.from_janus_object(janus_obj["input"])

        metadata = combine_metadata(obj["metadata"] for obj in janus_obj["outputs"])

        # Create a CodeBlock using the input text and metadata
        block = cls.get_empty()
        block.text = janus_obj["input"]
        block.start_byte = metadata["start_byte"]
        block.end_byte = metadata["end_byte"]
        block.start_point = (metadata["start_line"], metadata["start_char"])
        block.end_point = (metadata["end_line"], metadata["end_char"])
        if "input_tokens" in metadata:
            block.tokens = metadata["input_tokens"]
        return block

    def to_janus_object(self) -> JanusOutputObject:
        if self.previous_generation is not None:
            return self.previous_generation

        metadata: JanusMetadata = {
            "output_tokens": self.tokens,
            "start_line": self.start_point[0],
            "start_char": self.start_point[-1],
            "start_byte": self.start_byte,
            "end_line": self.end_point[0],
            "end_char": self.end_point[-1],
            "end_byte": self.end_byte,
            "language": self.language,
            "translation_complete": False,
        }

        janus_object: JanusOutputObject = {
            "input": self.complete_text,
            "metadata": metadata,
            "outputs": self.descendant_janus_objects() if self.children else [],
        }
        if self.text is not None:
            janus_object["output"] = self.complete_text
        return janus_object

    def descendant_janus_objects(self) -> list[JanusOutputObject]:
        if not self.children:
            return [self.to_janus_object()]
        return [obj for c in self.children for obj in c.descendant_janus_objects()]

    @classmethod
    def from_janus_object(cls, janus_obj: JanusOutputObject) -> "CodeBlock":
        return TranslatedCodeBlock.from_janus_object(janus_obj).to_codeblock()


class TranslatedCodeBlock(CodeBlock):
    """A class that represents the translated functional block of code.

    Attributes:
        original: The original code block.
        cost: The total cost to translate the original code block.
        translated: Whether this block has been successfully translated
    """

    def __init__(
        self,
        original: CodeBlock | None,
        language: str,
        converter: str | ForwardRef("Converter") | None = None,
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

        if original is None:
            original = CodeBlock.get_empty()
            previous_generation = None
        else:
            previous_generation = original.previous_generation

        super().__init__(
            id=original.id,
            name=original.name,
            node_type=original.node_type,
            language=language,
            text=None,
            start_point=original.start_point,
            end_point=original.end_point,
            start_byte=original.start_byte,
            end_byte=original.end_byte,
            tokens=0,
            children=[
                TranslatedCodeBlock(
                    original=child,
                    language=language,
                    converter=converter,
                    block_type=block_type,
                    block_label=block_label,
                )
                for child in original.children
            ],
            affixes=original.affixes,
            previous_generation=previous_generation,
            block_type=block_type,
            block_label=block_label,
        )
        self.omit_prefix = original.omit_prefix
        self.omit_suffix = original.omit_suffix

        self.original = original
        self.converter = converter

        self.model_name: str | None = model_name
        if converter is not None and not isinstance(converter, str):
            self.model_name = converter._model_name

        self.complete = original.complete
        self.translated = False
        self.cost = 0
        self.num_requests = 0
        self.tokens = 0
        self.processing_time = 0

        self.request_input_tokens = 0
        self.request_output_tokens = 0

    def __hash__(self) -> int:
        return hash((self.text, hash(self.original)))

    def __deepcopy__(self, memo) -> "CodeBlock":
        # Prevent the converter from getting duplicated by deepcopy,
        #  as this can cause issues with certain LLM objects
        deepcopy_method = self.__deepcopy__
        converter = self.converter
        self.__deepcopy__ = None
        self.converter = converter.__class__.__name__

        cp = deepcopy(self, memo)

        self.converter = converter
        cp.converter = converter
        self.__deepcopy__ = deepcopy_method
        cp.__deepcopy__ = deepcopy_method

        return cp

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

    def to_janus_object(self) -> JanusOutputObject:
        metadata: JanusMetadata = {
            "cost": self.total_cost,
            "processing_time": self.total_processing_time,
            "num_requests": self.total_num_requests,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.tokens,
            "request_input_tokens": self.total_request_input_tokens,
            "request_output_tokens": self.total_request_output_tokens,
            "start_line": self.start_point[0],
            "start_char": self.start_point[-1],
            "start_byte": self.start_byte,
            "end_line": self.end_point[0],
            "end_char": self.end_point[-1],
            "end_byte": self.end_byte,
            "language": self.language,
            "translation_complete": self.translation_completed,
        }

        if isinstance(self.converter, str):
            metadata["converter_name"] = self.converter
        elif self.converter is not None:
            metadata["converter_name"] = self.converter.__class__.__name__

        if self.model_name is not None:
            metadata["model_name"] = self.model_name
        if self.block_type is not None:
            metadata["type"] = self.block_type
        if self.block_label is not None:
            metadata["label"] = self.block_label

        janus_object: JanusOutputObject = {
            "input": self.previous_generation or self.original.text or "",
            "metadata": metadata,
            "outputs": self.descendant_janus_objects() if self.children else [],
        }
        if self.text is not None:
            janus_object["output"] = self.complete_text
        return janus_object

    @classmethod
    def from_janus_object(
        cls,
        janus_obj: JanusOutputObject,
    ) -> "TranslatedCodeBlock":
        metadata = janus_obj["metadata"]

        if isinstance(janus_obj["input"], str):
            original = None
        else:
            original = CodeBlock.from_janus_object(janus_obj["input"])

        translated_block = TranslatedCodeBlock(
            original=original,
            language=metadata["language"],
            converter=metadata.get("converter_name", None),
            model_name=metadata.get("model_name", None),
            block_type=metadata.get("type", None),
            block_label=metadata.get("label", None),
        )

        if not isinstance(janus_obj["input"], str):
            translated_block.previous_generation = janus_obj["input"]

        translated_block.translated = metadata["translation_complete"]
        if "output" in janus_obj:
            translated_block.text = janus_obj["output"]

        translated_block.children = [
            cls.from_janus_object(obj) for obj in janus_obj["outputs"]
        ]

        translated_block.cost = metadata.get("cost", 0.0)
        translated_block.processing_time = metadata.get("processing_time", 0.0)
        translated_block.num_requests = metadata.get("num_requests", 0)
        translated_block.request_input_tokens = metadata.get("request_input_tokens", 0)
        translated_block.request_output_tokens = metadata.get("request_output_tokens", 0)

        translated_block.tokens = metadata.get("output_tokens", 0)

        translated_block.start_byte = metadata.get("start_byte", 0)
        translated_block.end_byte = metadata.get("end_byte", -1)
        translated_block.start_point = (
            metadata.get("start_line", 0),
            metadata.get("start_char", 0),
        )
        translated_block.end_point = (
            metadata.get("end_line", -1),
            metadata.get("end_char", -1),
        )

        return translated_block

    def to_codeblock(self) -> CodeBlock:
        """Prepare this translated block to feed into a downstream Converter"""
        # The input to the next Converter is the entirety of this block
        start_line, start_char, start_byte = 0, 0, 0
        end_line, end_char, end_byte = -1, -1, -1
        if self.text is not None:
            input_lines = self.text.split("\n")
            end_line = len(input_lines) - 1
            end_char = len(input_lines[-1]) - 1
            end_byte = len(bytes(self.text, "utf-8")) - 1

        return CodeBlock(
            id=self.id,
            name=self.name,
            node_type=self.node_type,
            language=self.language,
            text=self.text,
            start_point=(start_line, start_char),
            start_byte=start_byte,
            end_point=(end_line, end_char),
            end_byte=end_byte,
            embedding_id=self.embedding_id,
            tokens=self.tokens,
            children=[child.to_codeblock() for child in self.children],
            affixes=self.affixes,
            previous_generation=self.to_janus_object(),
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


def codeblocks_to_janus_object(
    blocks: list[TranslatedCodeBlock | CodeBlock],
) -> JanusOutputObject:
    janus_objs = [b.to_janus_object() for b in blocks]
    return combine_janus_objects(janus_objs)


def combine_janus_objects(janus_objects: list[JanusOutputObject]) -> JanusOutputObject:
    if len(janus_objects) == 1:
        return janus_objects[0]

    if len(janus_objects) == 0:
        raise ValueError("Cannot combine zero objects")

    metadata = combine_metadata(obj["metadata"] for obj in janus_objects)

    inputs = [obj["input"] for obj in janus_objects]
    input_blocks = {}
    for input in inputs:
        if not input:
            continue

        if isinstance(input, str):
            block = CodeBlock.get_empty()
            block.text = input
        else:
            block = CodeBlock.from_janus_object(input)

        input_blocks[hash(block)] = block

    if len(input_blocks) == 1:
        input = list(input_blocks.values())[0]
    else:
        input = "MULTIPLE"

    janus_object: JanusOutputObject = {
        "input": input,
        "metadata": metadata,
        "outputs": janus_objects,
    }
    return janus_object
