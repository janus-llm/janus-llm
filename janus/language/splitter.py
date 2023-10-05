import re
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
        self._segment_leaves(root)
        self._merge_tree(root)

        return root

    def _get_ast(self, code: str) -> CodeBlock:
        """Build an abstract syntax tree of the given code, represented by a tree
        of CodeBlocks. Must be implemented in language-specific child classes.

        Arguments:
            code: The input file's code

        Returns:
            The root of a tree of CodeBlocks
        """
        raise NotImplementedError()

    def _set_identifiers(self, root: CodeBlock, path: Path):
        """Set the IDs and names of each node in the given tree. By default,
        node IDs take the form `child_<i>`, where <i> is an integer counter which
        increments in breadth-first order, and node names take the form
        `<filename>:<ID>`. Child classes should override this function to use
        more informative names based on the particular programming language.
        """
        seen_ids = 0
        queue = [root]
        while queue:
            node = queue.pop(0)  # BFS order to keep lower IDs toward the root
            node.id = f"child_{seen_ids}"
            seen_ids += 1
            node.name = f"{path.name}:{node.id}"
            queue.extend(node.children)

    def _merge_tree(self, root: CodeBlock):
        """Given the root of an abstract syntax tree represented in CodeBlocks,
        merge and prune nodes such that each constituent CodeBlock's text is
        short enough to fit in context (but no shorter), and that each byte of
        the represented code is present in the text of exactly one node in the
        tree.
        """
        stack = [root]
        while stack:
            node = stack.pop()
            self._merge_children(node)
            stack.extend(node.children)

    def _merge_children(self, node: CodeBlock):
        """Given a parent node in an abstract syntax tree, consolidate, merge,
        and prune its children such that this node's text fits into context,
        and does not overlap with the text represented by any of its children.
        After processing, this node's children will have been merged such that
        they maximally fit into LLM context. If the entire node text can fit
        into context, all its children will be pruned.
        """
        # If the text at the function input is less than the max tokens, then
        #  we can just return it as a CodeBlock with no children.
        if node.tokens <= self.max_tokens:
            node.children = []
            return

        node.complete = False

        # Consolidate nodes into groups, and then merge each group into a new node
        node_groups = self._group_nodes(node.children)
        node.children = list(map(self.merge_nodes, node_groups))

        # If not using placeholders, simply recurse for every child and delete
        #  this node's text and tokens
        if not self.use_placeholders:
            if not node.children:
                log.error(f"[{node.name}] Childless node too long for context!")
            node.text = None
            node.tokens = 0
            return

        text_chunks = [c.complete_placeholder for c in node.children]
        node.text = "".join(text_chunks)
        node.tokens = self._count_tokens(node.text)

        # If the text is still too long even with every child replaced with
        #  placeholders, there's no reason to bother with placeholders at all
        if node.tokens > self.max_tokens:
            node.text = None
            node.tokens = 0
            return

        sorted_indices: List[int] = sorted(
            range(len(node.children)),
            key=lambda idx: node.children[idx].tokens,
        )

        merged_child_indices = set()
        for idx in sorted_indices:
            child = node.children[idx]
            text_chunks[idx] = child.complete_text
            text = "".join(text_chunks)
            tokens = self._count_tokens(text)
            if tokens > self.max_tokens:
                break

            node.text = text
            node.tokens = tokens
            merged_child_indices.add(idx)

        # Remove all merged children from the child list
        node.children = [
            child
            for i, child in enumerate(node.children)
            if i not in merged_child_indices
        ]

    def _group_nodes(self, nodes: List[CodeBlock]) -> List[List[CodeBlock]]:
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
        nodes = sorted(nodes)
        text_chunks = [child.text for child in nodes]
        lengths = [node.tokens for node in nodes]

        # Estimate the length of each adjacent pair were they merged
        adj_sums = [lengths[i] + lengths[i + 1] for i in range(len(lengths) - 1)]

        groups = [[n] for n in nodes]
        while len(groups) > 1 and min(adj_sums) <= self.max_tokens:
            # Get the indices of the adjacent nodes that would result in the
            #  smallest possible merged snippet
            i0 = int(min(range(len(adj_sums)), key=adj_sums.__getitem__))
            i1 = i0 + 1

            # Recalculate the length. We can't simply use the adj_sum, because
            #  it is an underestimate due to the adjoining suffix/prefix.
            central_node = groups[i0][-1]
            merged_text = "".join([text_chunks[i0], central_node.suffix, text_chunks[i1]])
            merged_text_length = self._count_tokens(merged_text)

            # If the true length of the merged pair is too long, don't merge them
            #  Instead, correct the estimate, since shorter pairs may yet exist
            if merged_text_length > self.max_tokens:
                adj_sums[i0] = merged_text_length
                continue

            # Update adjacent sum estimates
            if i0 > 0:
                adj_sums[i0 - 1] += merged_text_length
            if i1 < len(adj_sums) - 1:
                adj_sums[i1 + 1] += merged_text_length

            # The potential merge length for this pair is removed
            adj_sums.pop(i0)

            # Merge the pair of node groups
            groups[i0 : i1 + 1] = [groups[i0] + groups[i1]]
            text_chunks[i0 : i1 + 1] = [merged_text]
            lengths[i0 : i1 + 1] = [merged_text_length]

        return groups

    def merge_nodes(self, nodes: List[CodeBlock]) -> CodeBlock:
        """Merge a list of nodes into a single node. The first and last nodes'
        respective prefix and suffix become this node's affixes.
        """
        if len(nodes) == 0:
            raise ValueError("Cannot merge zero nodes")

        if len(nodes) == 1:
            return nodes[0]

        languages = set(node.language for node in nodes)
        if len(languages) != 1:
            raise ValueError("Nodes have conflicting language")
        (language,) = languages

        # The prefix and suffix of the parent node are the prefix of the first
        #  child and the suffix of the last. Remove them from these children.
        prefix = nodes[0].pop_prefix()
        suffix = nodes[-1].pop_suffix()

        text = "".join(node.complete_text for node in nodes)
        name = f"{nodes[0].id}:{nodes[-1].id}"

        # Double check length (in theory this should never be an issue)
        tokens = self._count_tokens(text)
        if tokens > self.max_tokens:
            log.error(f"Merged node ({name}) too long for context!")

        return CodeBlock(
            text=text,
            name=name,
            id=name,
            start_point=nodes[0].start_point,
            end_point=nodes[-1].end_point,
            start_byte=nodes[0].start_byte,
            end_byte=nodes[-1].end_byte,
            affixes=(prefix, suffix),
            type=NodeType("merge"),
            children=sorted(sum([node.children for node in nodes], [])),
            language=language,
            tokens=tokens,
        )

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given text.

        Arguments:
            code: The text to count the number of tokens in.

        Returns:
            The number of tokens in the given text.
        """
        return self.model.get_num_tokens(code)

    def _segment_leaves(self, node: CodeBlock):
        """Given a root node, recurse to the leaf nodes of the tree and, if they
        do not fit in context, segment them into their constituent lines.
        The leaf nodes are updated in-place to hold a child for each
        non-whitespace line. If a leaf node already fits into context, it is
        left unchanged. Non-leaf nodes are not affected
        """
        if node.tokens <= self.max_tokens:
            return

        if node.children:
            for child in node.children:
                self._segment_leaves(child)
            return

        split_text = re.split(r"(\n+)", node.text)
        betweens = split_text[1::2]
        lines = split_text[::2]

        start_byte = node.start_byte
        node_line = 0
        for prefix, line, suffix in zip(betweens[:-1], lines, betweens[1:]):
            start_byte += len(bytes(prefix, "utf-8"))
            node_line += len(prefix)
            start_line = node.start_point[0] + node_line
            end_byte = start_byte + len(bytes(line, "utf-8"))
            end_char = len(line)

            name = f"{node.name}L#{node_line}"
            tokens = self._count_tokens(line)
            if tokens > self.max_tokens:
                raise TokenLimitError(r"Irreducible node too large for context!")

            node.children.append(
                CodeBlock(
                    text=line,
                    name=name,
                    id=name,
                    start_point=(start_line, 0),
                    end_point=(start_line, end_char),
                    start_byte=start_byte,
                    end_byte=end_byte,
                    affixes=(prefix, suffix),
                    type=NodeType("segment"),
                    children=[],
                    language=self.language,
                    tokens=tokens,
                )
            )
            start_byte = end_byte + len(suffix)
            node_line += len(suffix)

        # Keep the first child's prefix
        node.children[0].omit_prefix = False
