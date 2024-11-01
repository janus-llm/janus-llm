import re

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.node import NodeType
from janus.language.splitter import Splitter
from janus.llm.models_info import JanusModel
from janus.utils.logger import create_logger

log = create_logger(__name__)


class MumpsCombiner(Combiner):
    """A class that combines code blocks into mumps files."""

    def __init__(self) -> None:
        """Initialize a MumpsCombiner instance."""
        super().__init__("mumps")


class MumpsSplitter(Splitter):
    """A class for splitting MUMPS code into functional blocks to prompt
    with for transcoding.
    """

    # Consider labels to delimit subroutines. Labels (and only labels) start on
    #  column 1
    subroutine_pattern = re.compile(
        r"""
        (?:^          # Starting at either the beginning of the file...
          |\n    # ... or after the first newline after the last subroutine
        )\n*
        (.*?)           # Match the minimum amount of characters before...
        (?=           # ... a lookahead for:
          \s*(?:      # Any amount of whitespace followed by either...
            \n[^\s;$] # ... a newline and the start of the next label...
            | $       # ... OR the end of the file
          )
        )
        """,
        re.VERBOSE | re.DOTALL,
    )

    def __init__(
        self,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str] = ("routine_definition",),
        prune_node_types: tuple[str] = (),
        prune_unprotected: bool = False,
    ):
        """Initialize a MumpsSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="mumps",
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
        )

    def _set_identifiers(self, root: CodeBlock, name: str):
        stack = [root]
        while stack:
            node = stack.pop()
            node.name = f"{name}:{node.id}"
            stack.extend(node.children)

    def _get_ast(self, code: str) -> CodeBlock:
        subroutine_matches = self.subroutine_pattern.finditer(code)
        end_index = 0
        chunks = []
        betweens = []
        for match in subroutine_matches:
            i0 = match.start(1)
            i1 = match.end(1)
            if i0 < i1:
                betweens.append(code[end_index:i0])
                chunks.append(code[i0:i1])
                end_index = i1
        betweens.append(code[end_index:])

        start_line = 0
        start_byte = 0
        children = []
        for prefix, chunk, suffix in zip(betweens[:-1], chunks, betweens[1:]):
            start_byte += len(bytes(prefix, "utf-8"))
            start_line += prefix.count("\n")
            end_byte = start_byte + len(bytes(chunk, "utf-8"))
            end_line = start_line + chunk.count("\n")
            end_char = len(chunk) - chunk.rfind("\n") - 1

            # Set the node name to its label; if there is no label (which will
            #  only occur for the first chunk in the file
            label = re.search(r"^(\w+)", chunk)
            name = label.groups(1)[0] if label is not None else "anon"

            node = CodeBlock(
                text=chunk,
                name=name,
                id=name,
                start_point=(start_line, 0),
                end_point=(end_line, end_char),
                start_byte=start_byte,
                end_byte=end_byte,
                affixes=(prefix, suffix),
                node_type=NodeType("routine_definition"),
                children=[],
                language=self.language,
                tokens=self._count_tokens(chunk),
            )
            self._split_into_lines(node)
            for line_node in node.children:
                self._split_comment(line_node)

            children.append(node)

            start_byte = end_byte
            start_line = end_line

        return CodeBlock(
            text=code,
            name="root",
            id="root",
            start_point=(0, 0),
            end_point=(code.count("\n"), 0),
            start_byte=0,
            end_byte=len(bytes(code, "utf-8")),
            node_type=NodeType("routine"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )

    @staticmethod
    def comment_start(line: str) -> int:
        first_semicolon = line.find(";")
        if first_semicolon < 0:
            return first_semicolon

        # In mumps, quotes are escaped by doubling them (""). Single quote
        #  characters are logical not operators, not quotes
        n_quotes = line[:first_semicolon].replace('""', "").count('"')

        # If the number of quotes prior to the first semicolon is even, then
        #  that semicolon is not part of a quote (and therefore starts a comment)
        if n_quotes % 2 == 0:
            return first_semicolon

        last_semicolon = first_semicolon
        while (next_semicolon := line.find(";", last_semicolon + 1)) > 0:
            n_quotes = line[last_semicolon:next_semicolon].replace('""', "").count('"')

            # If the number of quotes in this chunk is odd, the total number
            #  of them up to this point is even, and the next semicolon begins
            #  the comment
            if n_quotes % 2:
                return next_semicolon

            last_semicolon = next_semicolon

        return -1

    def _split_comment(self, line_node: CodeBlock):
        comment_start = self.comment_start(line_node.text)
        if comment_start < 0:
            line_node.node_type = NodeType("code_line")
            return

        code = line_node.text[:comment_start]
        if not code.strip():
            line_node.node_type = NodeType("comment")
            return

        comment = line_node.text[comment_start:]
        (l0, c0), (l1, c1) = line_node.start_point, line_node.end_point
        prefix, suffix = line_node.affixes
        code_bytes = len(bytes(code, "utf-8"))

        line_node.children = [
            CodeBlock(
                text=code,
                name=f"{line_node.name}-code",
                id=f"{line_node.name}-code",
                start_point=(l0, c0),
                end_point=(l1, comment_start),
                start_byte=line_node.start_byte,
                end_byte=line_node.start_byte + code_bytes,
                node_type=NodeType("code_line"),
                children=[],
                language=line_node.language,
                tokens=self._count_tokens(code),
            ),
            CodeBlock(
                text=comment,
                name=f"{line_node.name}-comment",
                id=f"{line_node.name}-comment",
                start_point=(l0, c0 + comment_start),
                end_point=(l1, c1),
                start_byte=line_node.start_byte + code_bytes,
                end_byte=line_node.end_byte,
                node_type=NodeType("comment"),
                children=[],
                language=self.language,
                tokens=self._count_tokens(comment),
            ),
        ]
