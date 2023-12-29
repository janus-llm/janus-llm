from functools import total_ordering
from typing import ForwardRef, Hashable

from ..utils.logger import create_logger
from .node import NodeType

log = create_logger(__name__)


@total_ordering
class CodeBlock:
    """A class that represents a functional block of code.

    Attributes:
        id: The id of the code block in the AST
        name: Descriptive name of node
        type: The type of the code block ('function', 'module', etc.). Defined in the
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
        name: None | str,
        type: NodeType,
        language: str,
        text: None | str,
        start_point: None | tuple[int, int],
        end_point: None | tuple[int, int],
        start_byte: None | int,
        end_byte: None | int,
        tokens: int,
        children: list[ForwardRef("CodeBlock")],
        embedding_id: None | str = None,
        affixes: tuple[str, str] = ("", ""),
    ) -> None:
        self.id: Hashable = id
        self.name: None | str = name
        self.type: NodeType = type
        self.language: str = language
        self.text: None | str = text
        self.start_point: None | tuple[int, int] = start_point
        self.end_point: None | tuple[int, int] = end_point
        self.start_byte: None | [int] = start_byte
        self.end_byte: None | [int] = end_byte
        self.tokens: int = tokens
        self.children: list[ForwardRef("CodeBlock")] = sorted(children)
        self.embedding_id: None | [str] = embedding_id
        self.affixes: tuple[str, str] = affixes

        self.complete = True
        self.omit_prefix = True
        self.omit_suffix = False

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
        return f"{self.prefix}{self.text}{self.suffix}"

    @property
    def placeholder(self) -> str:
        return f"<<<{self.id}>>>"

    @property
    def complete_placeholder(self) -> str:
        return f"{self.prefix}<<<{self.id}>>>{self.suffix}"

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

    def tree_str(self, depth: int = 0) -> str:
        """A string representation of the tree with this block as the root

        Returns:
            A string representation of the tree with this block as the root
        """
        identifier = self.id
        if self.text is None:
            identifier = f"({identifier})"
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
                f"{'| '*depth}{identifier}{seg}",
                *[c.tree_str(depth + 1) for c in self.children],
            ]
        )


class TranslatedCodeBlock(CodeBlock):
    """A class that represents the translated functional block of code.

    Attributes:
        original: The original code block.
        cost: The total cost to translate the original code block.
        retries: The number of times translation had to be retried for this code
        translated: Whether this block has been successfully translated
    """

    def __init__(self, original: CodeBlock, language: str) -> None:
        """Create an "empty" `TranslatedCodeBlock` from the given original

        Arguments:
            original: The original code block
            language: The language to translate to

        Returns:
            A `TranslatedCodeBlock` with the same attributes as the original, except
            for `text`, `path`, `complete`, `language`, `tokens`, and `children`
        """
        super().__init__(
            id=original.id,
            name=original.name,
            type=original.type,
            language=language,
            text=None,
            start_point=original.start_point,
            end_point=original.end_point,
            start_byte=None,
            end_byte=None,
            tokens=0,
            children=[
                TranslatedCodeBlock(child, language) for child in original.children
            ],
            affixes=original.affixes,
        )
        self.original = original

        self.complete = original.complete
        self.translated = False
        self.cost = 0.0
        self.retries = 0

    @property
    def total_cost(self) -> float:
        """The total cost spent translating this block and all its descendents

        Returns:
            The total cost spent translating this block and all its descendents
        """
        return self.cost + sum(c.total_cost for c in self.children)

    @property
    def total_retries(self) -> int:
        """The total number of retries that were required to translate this block and
        all its descendents

        Returns:
            The total number of retries that were required to translate this block and
        """
        return self.retries + sum(c.total_retries for c in self.children)

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
