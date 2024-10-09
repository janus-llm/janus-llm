import re
from itertools import compress
from pathlib import Path
from typing import List

import tiktoken

from janus.language.block import CodeBlock
from janus.language.file import FileManager
from janus.language.node import NodeType
from janus.llm.models_info import JanusModel
from janus.utils.logger import create_logger

log = create_logger(__name__)


class TokenLimitError(Exception):
    """An exception raised when the token limit is exceeded and the code cannot be
    split into smaller blocks.
    """

    pass


class EmptyTreeError(Exception):
    """An exception raised when the tree is empty or does not exist (can happen
    when there are no nodes of interest in the tree)
    """

    pass


class FileSizeError(Exception):
    """An exception raised when the file size is too large for the splitter"""

    pass


class Splitter(FileManager):
    """A class for splitting code into functional blocks to prompt with for
    transcoding.
    """

    def __init__(
        self,
        language: str,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        skip_merge: bool = False,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        prune_unprotected: bool = False,
    ):
        """
        Arguments:
            language: The name of the language to split.
            model: The name of the model to use for counting tokens. If the model is None,
                will use tiktoken's default tokenizer to count tokens.
            max_tokens: The maximum number of tokens to use for each functional block.
            skip_merge: Whether to merge child nodes up to the max_token length.
                May be used for situations like documentation where function-level
                documentation is preferred.
                TODO: Maybe instead support something like a list of node types that
                      shouldnt be merged (e.g. functions, classes)?
            prune_unprotected: Whether to prune unprotected nodes from the tree.
        """
        super().__init__(language=language)
        self.model = model
        if self.model is None:
            self._encoding = tiktoken.get_encoding("cl100k_base")
        self.skip_merge = skip_merge
        self.max_tokens: int = max_tokens
        self._protected_node_types = set(protected_node_types)
        self._prune_node_types = set(prune_node_types)
        self.prune_unprotected = prune_unprotected

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        path = Path(file)
        code = path.read_text()
        return self.split_string(code, path.name)

    def split_string(self, code: str, name: str) -> CodeBlock:
        """Split the given code into functional code blocks.

        Arguments:
            code: The code as a string to split into functional blocks.
            name: The filename of the code block.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """

        root = self._get_ast(code)
        self._prune(root)
        if self.prune_unprotected:
            self._prune_unprotected(root)
        self._set_identifiers(root, name)
        self._segment_leaves(root)
        if not self.skip_merge:
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

    def _all_node_types(self, root: CodeBlock) -> set[NodeType]:
        types = set()
        stack = [root]
        while stack:
            node = stack.pop()
            types.add(node.node_type)
            stack.extend(node.children)
        return types

    def _set_identifiers(self, root: CodeBlock, name: str):
        """Set the IDs and names of each node in the given tree. By default,
        node IDs take the form `child_<i>`, where <i> is an integer counter which
        increments in breadth-first order, and node names take the form
        `<name>:<ID>`. Child classes should override this function to use
        more informative names based on the particular programming language.

        Arguments:
            root: The root of the tree to set identifiers for.
            name: The name of the file being split.
        """
        seen_ids = 0
        queue = [root]
        while queue:
            node = queue.pop(0)  # BFS order to keep lower IDs toward the root
            node.id = f"child_{seen_ids}"
            seen_ids += 1
            node.name = f"{name}:{node.id}"
            queue.extend(node.children)

    def _merge_tree(self, root: CodeBlock):
        """Given the root of an abstract syntax tree represented in CodeBlocks,
        merge and prune nodes such that each constituent CodeBlock's text is
        short enough to fit in context (but no shorter), and that each byte of
        the represented code is present in the text of exactly one node in the
        tree.
        """
        # Simulate recursion with a stack
        stack = [root]
        while stack:
            node = stack.pop()

            # If the text of this node can fit in context, then we can just
            #  prune its children, making it a leaf node.
            if node.tokens <= self.max_tokens and not self._has_protected_descendents(
                node
            ):
                node.children = []
                continue

            # Otherwise, this is an internal node. Mark it as incomplete, and
            #  drop its text (which will be represented in its children)
            node.complete = False
            node.text = None
            node.tokens = 0

            # If this node has no children but cannot fit into context, then we
            #  have a problem. Oversized nodes have already been segmented into
            #  lines, so this node contains a single line too long to send to
            #  the LLM. If this happens, the source code is probably malformed.
            # We have no choice but to log an error and simply ignore the node.
            if not node.children:
                log.error(f"[{node.name}] Childless node too long for context!")
                continue

            # Consolidate nodes into groups, and then merge each group into a new node
            node_groups = self._group_nodes(node.children)
            node.children = list(map(self.merge_nodes, node_groups))

            # "Recurse" by pushing the children onto the stack
            stack.extend(node.children)

    def _should_prune(self, node: CodeBlock) -> bool:
        return node.node_type in self._prune_node_types

    def _prune(self, root: CodeBlock) -> None:
        stack = [root]
        traversal = []
        while stack:
            node = stack.pop()
            traversal.append(node)
            node.children = [c for c in node.children if not self._should_prune(c)]
            stack.extend(node.children)

        for node in traversal[::-1]:
            node.rebuild_text_from_children()
            node.tokens = self._count_tokens(node.text)

    def _is_protected(self, node: CodeBlock) -> bool:
        return node.node_type in self._protected_node_types

    def _has_protected_descendents(self, node: CodeBlock) -> bool:
        if not self._protected_node_types:
            return False

        queue = [*node.children]
        while queue:
            node = queue.pop(0)
            if self._is_protected(node):
                return True
            queue.extend(node.children)
        return False

    def _prune_unprotected(self, root: CodeBlock) -> None:
        if not self._has_protected_descendents(root):
            if not self._is_protected(root):
                raise EmptyTreeError("No protected nodes in tree!")
            root.children = []
            return

        stack = [root]
        while stack:
            node = stack.pop()
            if self._is_protected(node):
                node.children = []
            node.children = [
                c
                for c in node.children
                if self._is_protected(c) or self._has_protected_descendents(c)
            ]
            stack.extend(node.children)

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

        # Create list of booleans parallel with adj_sums indicating whether that
        #  merge is allowed (according to the protected node types list)
        protected = list(map(self._is_protected, nodes))
        merge_allowed = [
            not (protected[i] or protected[i + 1]) for i in range(len(protected) - 1)
        ]

        groups = [[n] for n in nodes]
        while len(groups) > 1 and min(adj_sums) <= self.max_tokens and any(merge_allowed):
            # Get the indices of the adjacent nodes that would result in the
            #  smallest possible merged snippet. Ignore protected nodes.
            mergeable_indices = compress(range(len(adj_sums)), merge_allowed)
            i0 = int(min(mergeable_indices, key=adj_sums.__getitem__))
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

            if i0 > 0 and i1 < len(merge_allowed) - 1:
                if not (merge_allowed[i0 - 1] and merge_allowed[i1 + 1]):
                    merge_allowed[i0 - 1] = merge_allowed[i1 + 1] = False

            # The potential merge length for this pair is removed
            adj_sums.pop(i0)
            merge_allowed.pop(i0)

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
            log.error(
                f"Merged node ({name}) too long for context!"
                f" ({tokens} > {self.max_tokens})"
            )

        return CodeBlock(
            text=text,
            name=name,
            id=name,
            start_point=nodes[0].start_point,
            end_point=nodes[-1].end_point,
            start_byte=nodes[0].start_byte,
            end_byte=nodes[-1].end_byte,
            affixes=(prefix, suffix),
            node_type=NodeType("merge"),
            children=sorted(sum([node.children for node in nodes], [])),
            language=language,
            tokens=tokens,
        )

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given text.

        Will use tiktoken if a model is not specified.

        Arguments:
            code: The text to count the number of tokens in.

        Returns:
            The number of tokens in the given text.
        """
        if self.model is not None:
            return self.model.get_num_tokens(code)
        else:
            return len(self._encoding.encode(code))

    def _segment_leaves(self, node: CodeBlock):
        """Given a root node, recurse to the leaf nodes of the tree and, if they
        do not fit in context, segment them into their constituent lines.
        The leaf nodes are updated in-place to hold a child for each
        non-whitespace line. If a leaf node already fits into context, it is
        left unchanged. Non-leaf nodes are not affected
        """
        if node.tokens <= self.max_tokens:
            return

        if self._is_protected(node):
            log.error(
                "Protected node too large for context!"
                f" ({node.tokens} > {self.max_tokens})"
            )

        if node.children:
            for child in node.children:
                self._segment_leaves(child)
            return

        if node.start_point is None or node.end_point is None:
            raise ValueError("Node has no start or end point")

        self._split_into_lines(node)

    def _split_into_lines(self, node: CodeBlock):
        split_text = re.split(r"(\n+)", node.text)

        # If the string didn't start/end with newlines, make sure to include
        #  empty strings for the prefix/suffixes
        if split_text[0].strip("\n"):
            split_text = [""] + split_text
        if split_text[-1].strip("\n"):
            split_text.append("")
        betweens = split_text[::2]
        lines = split_text[1::2]

        start_byte = node.start_byte
        node_line = 0
        for prefix, line, suffix in zip(betweens[:-1], lines, betweens[1:]):
            start_byte += len(bytes(prefix, "utf-8"))
            node_line += len(prefix)
            start_line = node.start_point[0] + node_line
            end_byte = start_byte + len(bytes(line, "utf-8"))
            end_char = len(line)

            name = f"{node.name}-L#{node_line}"
            tokens = self._count_tokens(line)
            if tokens > self.max_tokens:
                log.error(
                    "Irreducible node too large for context!"
                    f" ({tokens} > {self.max_tokens})"
                )

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
                    node_type=NodeType(f"{node.node_type}__segment"),
                    children=[],
                    language=self.language,
                    tokens=tokens,
                )
            )
            start_byte = end_byte

        # Keep the first child's prefix
        node.children[0].omit_prefix = False
