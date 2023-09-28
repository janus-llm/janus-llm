import dataclasses
from typing import ForwardRef, Hashable, List, Optional, Tuple

from ..utils.logger import create_logger
from .node import NodeType

log = create_logger(__name__)


@dataclasses.dataclass
class CodeBlock:
    """A class that represents a functional block of text.

    Attributes:
        text: The text block.
        path: The path to the file containing the text block.
        complete: Whether or not the text block is complete. If it isn't complete, it
                  should have children components. This means that this text block has
                  missing sections inside of it that are in its children.
        start_line: The line number of the first line of the text block.
        end_line: The line number of the last line of the text block.
        language: The language of the text block.
        type: The type of the text block ('function', 'module', etc.). Defined in the
              language-specific modules.
        tokens: The number of tokens in the text block.
        depth: The depth of the text block in the AST.
        id: The id of the text block in the AST
        children: A tuple of child text blocks.
    """

    id: Hashable
    name: Optional[str]
    type: NodeType
    complete: bool
    language: str
    text: Optional[str]
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    start_byte: int
    end_byte: int
    prefix: str
    suffix: str
    tokens: int
    children: List[ForwardRef("CodeBlock")]

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
    def total_tokens(self) -> int:
        """The total tokens represented by this block and all its descendents

        Returns:
            The total number of tokens represented by this block and all its
            descendents
        """
        return self.tokens + sum(c.total_tokens for c in self.children)

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
        start = f"{self.start_point[0]}:{self.start_point[1]}"
        end = f"{self.end_point[0]}:{self.end_point[1]}"
        return "\n".join(
            [
                f"{'| '*depth}{identifier} [{start}-{end}]",
                *[c.tree_str(depth+1) for c in self.children],
            ]
        )


@dataclasses.dataclass
class TranslatedCodeBlock(CodeBlock):
    """A class that represents the translated functional block of text.

    Attributes:
        original: The original text block.
        cost: The total cost to translate the original text block.
        retries: The number of times translation had to be retried for this text
        translated: Whether this block has been successfully translated
    """

    original: CodeBlock
    cost: float = 0.0
    retries: int = 0
    translated: bool = False

    @classmethod
    def from_original(
        cls, original: CodeBlock, language: str
    ) -> ForwardRef("TranslatedCodeBlock"):
        """Create an "empty" `TranslatedCodeBlock` from the given original

        Arguments:
            original: The original text block
            language: The language to translate to

        Returns:
            A `TranslatedCodeBlock` with the same attributes as the original, except
            for `text`, `path`, `complete`, `language`, `tokens`, and `children`
        """
        block = cls(**dataclasses.asdict(original), original=original)
        return dataclasses.replace(
            block,
            text=None,
            complete=False,
            language=language,
            tokens=0,
            children=[],
        )

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
        return self.total_input_tokens / self.original.total_tokens
