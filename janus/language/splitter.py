from pathlib import Path
from typing import List

from langchain.schema.language_model import BaseLanguageModel

from ..utils.logger import create_logger
from .block import CodeBlock
from .file import FileManager
from .node import NodeType

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
        use_placeholders: bool = True,
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
        path = Path(file)
        code = path.read_text()

        root = self._get_ast(code)
        self._set_identifiers(root, path)

        self._recurse_split(root)
        log.debug(f"[{root.name}] CodeBlock Structure:\n{root.tree_str()}")

        return root

    def _get_ast(self, code: str | bytes) -> CodeBlock:
        raise NotImplementedError()

    def _set_identifiers(self, root: CodeBlock, path: Path):
        seen_ids = 0
        queue = [root]
        while queue:
            node = queue.pop(0)  # BFS order to keep lower IDs toward the root
            node.id = f"child_{seen_ids}"
            seen_ids += 1
            node.name = f"{path.name}:{node.id}"
            queue.extend(node.children)

    def _recurse_split(
        self,
        node: CodeBlock
    ):
        """Recursively split the code into functional blocks.

        Arguments:
            node: The current node in the tree.
        """
        # First get the code for all the siblings at this level
        text = node.text
        length = self._count_tokens(text)

        # If the text at the function input is less than the max tokens, then
        #  we can just return it as a CodeBlock with no children.
        if length < self.max_tokens:
            node.children = []
            return

        node.complete = False

        # Consolidate nodes into groups, and then merge each group into a new node
        node_groups = self._consolidate_nodes(node.children)
        node.children = list(map(self.merge_nodes, node_groups))

        # Create list of this node's component texts (excluding its own prefix/suffix)
        text_chunks = [c.text + c.suffix for c in node.children]
        text_chunks[0] = node.children[0].prefix + text_chunks[0]

        lengths = list(map(self._count_tokens, text_chunks))
        remaining_indices: List[int] = list(range(len(lengths)))
        remaining_indices.sort(key=lengths.__getitem__)

        # Replace child node text with placeholders until we can fit in context,
        #  starting with the longest children
        while remaining_indices and (node.tokens > self.max_tokens or not self.use_placeholders):
            # Remaining indices is sorted by text length, ascending
            longest_index = remaining_indices.pop()
            longest_child = node.children[longest_index]
            self._recurse_split(longest_child)

            text_chunks[longest_index] = f"<<<{longest_child.id}>>>"
            node.text = "".join(text_chunks)
            node.tokens = self._count_tokens(node.text)

        # Any remaining children will be represented in this node's text, including
        #  their prefixes and suffixes. Therefore, remove the prefixes of the
        #  adjacent children (only the first child's prefix was included in
        #  the text chunks, so suffixes need not be removed)
        for i in remaining_indices:
            if i < len(node.children)-1:
                node.children[i+1].prefix = ""

        # Any remaining children can be pruned, as their content is represented
        #  in this node's text. This must be done in reverse order to that the
        #  indices don't change due to the deletion
        for i in sorted(remaining_indices, reverse=True):
            del node.children[i]

        # If the text is still too long, then every child has already been
        #  replaced with a placeholder. Therefore, even if placeholders are
        #  enabled, there is no benefit to using them for this node
        if not self.use_placeholders or node.tokens > self.max_tokens:
            node.text = None
            node.tokens = 0
            return

    def _consolidate_nodes(self, nodes: List[CodeBlock]) -> List[List[CodeBlock]]:
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
        nodes = sorted(nodes, key=lambda node: node.start_byte)
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

    def merge_nodes(self, nodes: List[CodeBlock]) -> CodeBlock:
        if len(nodes) == 0:
            raise ValueError("Cannot merge zero nodes")

        if len(nodes) == 1:
            return nodes[0]

        languages = set(node.language for node in nodes)
        if len(languages) != 1:
            raise ValueError("Nodes have conflicting language")
        (language,) = languages

        interleaved = [s for node in nodes for s in [node.text, node.suffix]]
        text = "".join(interleaved[:-1])
        id = f"{nodes[0].id}:{nodes[-1].id}"
        return CodeBlock(
            text=text,
            name=id,
            id=id,
            start_point=nodes[0].start_point,
            end_point=nodes[-1].end_point,
            start_byte=nodes[0].start_byte,
            end_byte=nodes[-1].end_byte,
            prefix=nodes[0].prefix,
            suffix=nodes[-1].suffix,
            type=NodeType("merge"),
            children=sum([node.children for node in nodes], []),
            language=language,
            tokens=self._count_tokens(text),
            complete=all(node.complete for node in nodes)
        )

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given text.

        Arguments:
            code: The text to count the number of tokens in.

        Returns:
            The number of tokens in the given text.
        """
        return self.model.get_num_tokens(code)
