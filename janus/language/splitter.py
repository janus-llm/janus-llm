import platform
from pathlib import Path
from typing import Hashable, Optional, Callable, List
from math import sqrt

import tree_sitter
from git import Repo
from langchain.schema.language_model import BaseLanguageModel

from ..utils.logger import create_logger
from .node import NodeType
from .block import CodeBlock
from .file import FileManager

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

    def __init__(self, language: str, model: BaseLanguageModel, max_tokens: int = 4096):
        """
        Arguments:
            max_tokens: The maximum number of tokens to use for each functional block.
            model: The name of the model to use for translation.
        """
        super().__init__(language=language)
        # Divide max_tokens by 3 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        self.model = model

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        path = Path(file)
        code = path.read_text()
        block = self._split(code, path)
        return block

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
        if isinstance(code, str):
            code = bytes(code, "utf-8")

        tree = self.parser.parse(code)
        cursor = tree.walk()

        seen_ids = set()
        def id_gen():
            block_id = f"<<<child_{len(seen_ids)}>>>"
            seen_ids.add(block_id)
            return block_id

        return self._recurse_split(
            node=cursor.node,
            path=path,
            depth=0,
            parent_id=None,
            id_gen=id_gen
        )

    def _recurse_split(
            self,
            node: tree_sitter.Node,
            path: Path,
            depth: int,
            parent_id: Optional[Hashable],
            id_gen: Callable[[], Hashable]
        ) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            node: The current node in the tree.
            path: The path to the file containing the code.
            depth: The current depth of the recursion.
            parent_id: The id of the calling parent
            id_gen: A function with which to generate child ids

        Returns:
            A CodeBlock object.
        """
        # First get the text for all the siblings at this level
        text = node.text.decode()
        block_length = self._count_tokens(text)
        node_id = id_gen()

        # If the text at the function input is less than the max tokens, then
        #  we can just return it as a CodeBlock with no children.
        if self._count_tokens(text) < self.max_tokens:
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
                tokens=block_length,
            )

        node_groups = self._consolidate_nodes(node.children, depth)
        text_chunks = ['\n'.join(c.text.decode() for c in group) for group in node_groups]
        lengths = list(map(self._count_tokens, text_chunks))
        remaining_indices = sorted(range(len(lengths)), key=lengths.__getitem__)

        # Replace child node code with placeholders until we can fit in context,
        #  starting with the longest children
        child_blocks = []
        while remaining_indices and self._count_tokens('\n'.join(text_chunks)) > self.max_tokens:
            # Remaining indices is sorted by code length, ascending
            longest_index = remaining_indices.pop()
            group = node_groups[longest_index]

            # Multi-node groups are guaranteed to be within context length
            if len(group) > 1:
                code = '\n'.join(c.text.decode() for c in group)
                length = self._count_tokens(code)
                child = CodeBlock(
                    code=code,
                    path=path,
                    complete=True,
                    start_line=group[0].start_point[0],
                    end_line=group[-1].end_point[0],
                    depth=depth + 1,
                    id=id_gen(),
                    parent_id=node_id,
                    children=[],
                    language=self.language,
                    type=node.type,
                    tokens=length,
                )

            # Recursively split singleton nodes
            else:
                child = self._recurse_split(
                    node=group[0],
                    path=path,
                    depth=depth+1,
                    parent_id=node_id,
                    id_gen=id_gen
                )
            text_chunks[longest_index] = f"{self.comment} {child.id}"
            child_blocks.append(child)

        if self._count_tokens('\n'.join(text_chunks)) <= self.max_tokens:
            return CodeBlock(
                code='\n'.join(text_chunks),
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
                tokens=block_length,
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
            group = grandchild_blocks[i:i+group_size]
            code = '\n'.join(text_chunks[i:i+group_size])
            length = sum(c.tokens for c in group)
            child = CodeBlock(
                code=code,
                path=path,
                complete=False,
                start_line=group[0].start_line,
                end_line=group[-1].end_line,
                depth=depth,
                id=id_gen(),
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
            tokens=block_length,
        )

    def _consolidate_nodes(self, nodes: List[tree_sitter.Node], depth) -> List[List[tree_sitter.Node]]:
        text_chunks = [child.text.decode() for child in nodes]
        lengths = list(map(self._count_tokens, text_chunks))

        # Estimate the length of each adjacent pair were they merged
        adj_sums = [lengths[i] + lengths[i+1] for i in range(len(lengths)-1)]

        groups = [[n] for n in nodes]
        while len(groups) > 1 and min(adj_sums) <= self.max_tokens:
            # Get the indices of the adjacent nodes that would result in the
            #  smallest possible merged snippet
            i0 = int(min(range(len(adj_sums)), key=adj_sums.__getitem__))
            i1 = i0 + 1

            # Merge the pair of node groups
            groups[i0:i1+1] = [groups[i0] + groups[i1]]

            # Recalculate the length. We can't simply use the adj_sum, because
            #  it is an underestimate due to the added newline.
            #  In testing, the length of a merged pair is between 2 and 3 tokens
            #  longer than the sum of the individual lengths, on average.
            text_chunks[i0:i1+1] = [text_chunks[i0] + '\n' + text_chunks[i1]]
            lengths[i0:i1+1] = [self._count_tokens(text_chunks[i0])]

            # The potential merge length for this pair is removed
            adj_sums.pop(i0)

            # Update adjacent sum estimates
            if i0 > 0:
                adj_sums[i0-1] = lengths[i0-1] + lengths[i0]
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

    def _git_clone(self, repository_url: str, destination_folder: Path | str) -> None:
        try:
            Repo.clone_from(repository_url, destination_folder)
            log.debug(f"{repository_url} cloned to {destination_folder}")
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _create_parser(
        self, so_file: Path | str, github_url: str, tree_sitter_lang_dir: str
    ) -> None:
        """Create the parser for the given language.

        Arguments:
            so_file: The path to the so file for the language.
        """
        tree_sitter_dir = Path.home() / ".tree-sitter"
        tree_sitter_dir.mkdir(exist_ok=True)
        lang_dir = tree_sitter_dir / tree_sitter_lang_dir

        if not lang_dir.exists():
            self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(
            # Store the library in the `build` directory
            str(so_file),
            [str(lang_dir)],
        )

    def _load_parser(self, build_dir: Path, github_url: str) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.

        Arguments:
            build_dir: The directory to store the so file in.
            github_url: The url to the tree-sitter GitHub repository for the language.
        """
        so_filename = (
            f"{self.language}_parser_{platform.system()}_{platform.processor()}.so"
        )
        so_file = (build_dir / so_filename).__str__()
        try:
            self.parser.set_language(tree_sitter.Language(so_file, self.language))
        except OSError:
            log.warning(
                f"Could not load {so_file}, building one for {platform.system()} "
                f"system, with {platform.processor()} processor"
            )
            self._create_parser(so_file, github_url, f"tree-sitter-{self.language}")
            self._load_parser(build_dir, github_url)
