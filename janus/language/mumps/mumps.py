import re
from pathlib import Path

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..combine import Combiner
from ..node import NodeType
from ..splitter import Splitter

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

    def __init__(self, model: None | BaseLanguageModel = None, max_tokens: int = 4096):
        """Initialize a MumpsSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="mumps",
            model=model,
            max_tokens=max_tokens,
            use_placeholders=False,
        )

        # MUMPS code tends to take about 2/3 the space of Python
        self.max_tokens: int = int(max_tokens * 2 / 5)

    def _set_identifiers(self, root: CodeBlock, path: Path):
        stack = [root]
        while stack:
            node = stack.pop()
            node.name = f"{path.name}:{node.id}"
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
                type=NodeType("subroutine"),
                children=[],
                language=self.language,
                tokens=self._count_tokens(chunk),
            )
            children.append(node)

            start_byte = end_byte + len(bytes(suffix, "utf-8"))
            start_line = end_line + suffix.count("\n")

        return CodeBlock(
            text=code,
            name="root",
            id="root",
            start_point=(0, 0),
            end_point=(code.count("\n"), 0),
            start_byte=0,
            end_byte=len(bytes(code, "utf-8")),
            type=NodeType("routine"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )
