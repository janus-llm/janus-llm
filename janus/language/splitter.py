from math import sqrt
from pathlib import Path
from typing import Hashable, List, Optional

from langchain.schema.language_model import BaseLanguageModel

from ..utils.logger import create_logger
from .block import CodeBlock
from .file import FileManager
from .node import NodeType, ASTNode

log = create_logger(__name__)


class TokenLimitError(Exception):
    """An exception raised when the token limit is exceeded and the code cannot be
    split into smaller blocks.
    """

    pass


class Splitter(FileManager):
    """A class for splitting code into functional blocks to prompt with for
    transcoding.
    """

    def __init__(
        self,
        language: str,
        model: BaseLanguageModel,
        max_tokens: int = 4096,
        use_placeholders: bool = True
    ):
        """
        Arguments:
            max_tokens: The maximum number of tokens to use for each functional block.
            model: The name of the model to use for translation.
        """
        super().__init__(language=language)
        self.model = model
        self.use_placeholders = use_placeholders

        # Divide max_tokens by 3 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        self._reset_id_function()
        path = Path(file)
        code = path.read_text()
        block = self._split(code, path)
        log.debug(f"Tree Structure:\n{block.tree_str}")
        return block

    def _reset_id_function(self) -> None:
        self.seen_ids = set()

    def _generate_id(self, *args, **kwargs) -> Hashable:
        block_id = f"<<<child_{len(self.seen_ids)}>>>"
        self.seen_ids.add(block_id)
        return block_id

    def _get_ast(self, code: str | bytes) -> ASTNode:
        raise NotImplementedError()

    def _split(self, code: str | bytes, path: Path) -> CodeBlock:
        """Use tree-sitter to walk through the code and split into functional code blocks.

        The functional code blocks will have children if each individual code block
        doesn't fit within `self.max_tokens`.

        Arguments:
            code: The code to split up.
            path: The path to the file containing the code.

        Returns:
            A nested `CodeBlock`.
        """
        root = self._get_ast(code)
        return self._recurse_split(
            node=root,
            path=path,
            depth=0,
            parent_id=None,
            use_placeholders=self.use_placeholders
        )

    def _recurse_split(
        self,
        node: ASTNode,
        path: Path,
        depth: int,
        parent_id: Optional[Hashable],
        use_placeholders: bool = True,
    ) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            node: The current node in the tree.
            path: The path to the file containing the code.
            depth: The current depth of the recursion.
            parent_id: The id of the calling parent
            use_placeholders: Whether to use placeholders

        Returns:
            A `CodeBlock` object.
        """
        # First get the text for all the siblings at this level
        text = node.text
        length = self._count_tokens(text)
        node_id = self._generate_id(node)

        # If the text at the function input is less than the max tokens, then
        #  we can just return it as a CodeBlock with no children.
        if length < self.max_tokens:
            return CodeBlock(
                code=text,
                path=path,
                complete=True,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                depth=depth,
                id=node_id,
                parent_id=parent_id,
                children=[],
                language=self.language,
                type=node.type,
                tokens=length,
            )

        node_groups = self._consolidate_nodes(node.children)
        text_chunks = ["\n".join(c.text for c in group) for group in node_groups]
        lengths = list(map(self._count_tokens, text_chunks))
        remaining_indices = sorted(range(len(lengths)), key=lengths.__getitem__)

        code = "\n".join(text_chunks)
        length = self._count_tokens(code)

        # Replace child node code with placeholders until we can fit in context,
        #  starting with the longest children
        child_blocks = []
        while remaining_indices and (length > self.max_tokens or not use_placeholders):
            # Remaining indices is sorted by code length, ascending
            longest_index = remaining_indices.pop()
            group = node_groups[longest_index]
            group_node = ASTNode.merge_nodes(group)

            child = self._recurse_split(
                node=group_node,
                path=path,
                depth=depth + 1,
                parent_id=node_id,
                use_placeholders=use_placeholders
            )

            text_chunks[longest_index] = f"{self.comment} {child.id}"
            child_blocks.append(child)

            code = "\n".join(text_chunks)
            length = self._count_tokens(code)

        if length <= self.max_tokens or not use_placeholders:
            return CodeBlock(
                code=code if use_placeholders else None,
                path=path,
                complete=False,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                depth=depth,
                id=node_id,
                parent_id=parent_id,
                children=child_blocks,
                language=self.language,
                type=node.type,
                tokens=length if use_placeholders else 0,
            )

        # If we never brought code down to size, the entire file currently
        #  consists of placeholders, and children need to be grouped
        # TODO: It is extremely likely, but possible, that the resulting code
        #  may still be too long to fit in the context window. Technically this
        #  should be moved to a recursive function to handle that.
        # Make sure the blocks are sorted by position in the file
        grandchild_blocks = sorted(child_blocks, key=lambda b: b.start_line)
        child_blocks = []

        # Split into sqrt(N) groups
        group_size = int(sqrt(len(grandchild_blocks)))
        for i in range(0, len(grandchild_blocks), group_size):
            group = grandchild_blocks[i : i + group_size]
            code = "\n".join(text_chunks[i : i + group_size])
            length = sum(c.tokens for c in group)
            child = CodeBlock(
                code=code,
                path=path,
                complete=False,
                start_line=group[0].start_line,
                end_line=group[-1].end_line,
                depth=depth,
                id=self._generate_id(node),
                parent_id=node_id,
                children=group,
                language=self.language,
                type=NodeType("subdivision"),
                tokens=length,
            )

            # Update grandchildren's parent ids to the inserted child's id
            for grandchild in child.children:
                grandchild.parent_id = child.id

            child_blocks.append(child)

        # Increase the depth of all ancestors
        descendents = child_blocks.copy()
        while descendents:
            b = descendents.pop()
            b.depth += 1
            descendents.extend(b.children)

        return CodeBlock(
            code=None,
            path=path,
            complete=False,
            start_line=node.start_point[0],
            end_line=node.end_point[0],
            depth=depth,
            id=node_id,
            parent_id=parent_id,
            children=child_blocks,
            language=self.language,
            type=node.type,
            tokens=0,
        )

    def _consolidate_nodes(
        self, nodes: List[ASTNode]
    ) -> List[List[ASTNode]]:
        """Consolidate a list of tree_sitter nodes into groups. Each group should fit
        into the context window, with the exception of single-node groups which may be
        too long to fit on their own. This ensures that nodes with many many short
        children are not translated one child at a time, instead packing as many children
        adjacent snippets as possible into context.

        This function attempts to efficiently pack nodes, but is not optimal.

        Arguments:
            nodes: A list of tree_sitter nodes

        Returns:
            A list of lists. Each list consists of one or more nodes. This structure is
            ordered such that, were it flattened, all nodes would be sorted according to
            appearance in the original file.
        """
        nodes = sorted(nodes, key=lambda node: node.start_point)
        text_chunks = [child.text for child in nodes]
        lengths = list(map(self._count_tokens, text_chunks))

        # Estimate the length of each adjacent pair were they merged
        adj_sums = [lengths[i] + lengths[i + 1] for i in range(len(lengths) - 1)]

        groups = [[n] for n in nodes]
        while len(groups) > 1 and min(adj_sums) <= self.max_tokens:
            # Get the indices of the adjacent nodes that would result in the
            #  smallest possible merged snippet
            i0 = int(min(range(len(adj_sums)), key=adj_sums.__getitem__))
            i1 = i0 + 1

            # Merge the pair of node groups
            groups[i0 : i1 + 1] = [groups[i0] + groups[i1]]

            # Recalculate the length. We can't simply use the adj_sum, because
            #  it is an underestimate due to the added newline.
            #  In testing, the length of a merged pair is between 2 and 3 tokens
            #  longer than the sum of the individual lengths, on average.
            text_chunks[i0 : i1 + 1] = [text_chunks[i0] + "\n" + text_chunks[i1]]
            lengths[i0 : i1 + 1] = [self._count_tokens(text_chunks[i0])]

            # The potential merge length for this pair is removed
            adj_sums.pop(i0)

            # Update adjacent sum estimates
            if i0 > 0:
                adj_sums[i0 - 1] = lengths[i0 - 1] + lengths[i0]
            if i0 < len(adj_sums):
                adj_sums[i0] += lengths[i0] + lengths[i1]

        return groups

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given code.

        Arguments:
            code: The code to count the number of tokens in.

        Returns:
            The number of tokens in the given code.
        """
        return self.model.get_num_tokens(code)
