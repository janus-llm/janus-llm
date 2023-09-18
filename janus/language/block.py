import dataclasses
from pathlib import Path
from typing import ForwardRef, Hashable, List, Optional

from ..utils.logger import create_logger
from .node import NodeType

log = create_logger(__name__)


@dataclasses.dataclass
class CodeBlock:
    """A class that represents a functional block of code.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete. If it isn't complete, it
                  should have children components. This means that this code block has
                  missing sections inside of it that are in its children.
        start_line: The line number of the first line of the code block.
        end_line: The line number of the last line of the code block.
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.). Defined in the
              language-specific modules.
        tokens: The number of tokens in the code block.
        depth: The depth of the code block in the AST.
        id: The id of the code block in the AST
        children: A tuple of child code blocks.
    """

    code: Optional[str]
    path: Optional[Path]
    complete: bool
    start_line: int
    end_line: int
    language: str
    type: NodeType
    tokens: int
    depth: int
    id: Hashable
    parent_id: Optional[Hashable]
    children: List[ForwardRef("CodeBlock")]

    @property
    def n_descendents(self):
        """ The total number of ancestors of this block"""
        return 1 + sum(c.n_descendents for c in self.children)

    @property
    def height(self):
        """ The number of edges between this node and a leaf """
        return 1 + max(c.height for c in self.children) if self.children else 0

    @property
    def total_tokens(self):
        """ The total tokens represented by this block and all its descendents"""
        return self.tokens + sum(c.total_tokens for c in self.children)

    @property
    def tree_str(self):
        """ A string representation of the tree with this block as the root"""
        return "\n".join(
            [
                f"{'| '*self.depth}{self.id}{'*' if self.code is None else ''}",
                *[c.tree_str for c in self.children],
            ]
        )


@dataclasses.dataclass
class TranslatedCodeBlock(CodeBlock):
    """A class that represents the translated functional block of code.

    Attributes:
        original: The original code block.
        cost: The total cost to translate the original code block.
        retries: The number of times translation had to be retried for this code
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
        """ Create an "empty" TranslatedCodeBlock from the given original"""
        block = cls(**dataclasses.asdict(original), original=original)
        return dataclasses.replace(
            block,
            code=None,
            path=None,
            complete=False,
            language=language,
            tokens=0,
            children=[],
        )

    @property
    def total_cost(self):
        """ The total cost spent translating this block and all its descendents"""
        return self.cost + sum(c.total_cost for c in self.children)

    @property
    def total_retries(self):
        """ The total number of retries that were required to translate this
            block and all its descendents
        """
        return self.retries + sum(c.total_retries for c in self.children)

    @property
    def total_input_tokens(self):
        """ The total number of input tokens represented by this block and
            all its successfully-translated descendents
        """
        children_sum = sum(c.total_input_tokens for c in self.children)
        return children_sum + (self.original.tokens if self.translated else 0)

    @property
    def translation_completeness(self):
        """ The share of the input that was successfully translated"""
        return self.total_input_tokens / self.original.total_tokens


