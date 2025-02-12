from functools import total_ordering
from typing import TYPE_CHECKING, ForwardRef, Hashable, Optional, Tuple

from janus.language.node import NodeType
from janus.utils.logger import create_logger

if TYPE_CHECKING:
    from janus.converter.converter import Converter

log = create_logger(__name__)


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
        children: list[ForwardRef("CodeBlock")],
        embedding_id: Optional[str] = None,
        affixes: Tuple[str, str] = ("", ""),
        context_tags: dict[str, str] = {},
        previous_generations: list["TranslatedCodeBlock"] = [],
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
        self.children: list[ForwardRef("CodeBlock")] = sorted(children)
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

    def __lt__(self, other: ForwardRef("CodeBlock")) -> bool:
        return (self.start_byte, self.end_byte) < (other.start_byte, other.end_byte)

    def __eq__(self, other: ForwardRef("CodeBlock")) -> bool:
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
        identifier = self.id
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
        converter: ForwardRef("Converter"),
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
                TranslatedCodeBlock(child, language, block_type, block_label)
                for child in original.children
            ],
            affixes=original.affixes,
            previous_generations=original.previous_generations,
            block_type=block_type,
            block_label=block_label,
        )

        self.original = original
        self.converter = converter

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

    def to_codeblock(self) -> CodeBlock:
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
            previous_generations=self.previous_generations + [self],
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
        previous_generations: list[ForwardRef("BlockCollection")] = [],
    ):
        self.blocks = blocks
        self.previous_generations = previous_generations

    def to_codeblock(self) -> ForwardRef("BlockCollection"):
        return BlockCollection(
            [b.to_codeblock() for b in self.blocks], self.previous_generations + [self]
        )

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
