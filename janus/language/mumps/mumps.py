import re
from typing import List
from pathlib import Path

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..combine import Combiner
from ..node import NodeType
from ..splitter import Splitter
from ..block import CodeBlock

log = create_logger(__name__)


class MumpsCombiner(Combiner):
    """A class that combines text blocks into mumps files."""

    def __init__(self) -> None:
        """Initialize a MumpsCombiner instance."""
        super().__init__("mumps")


class MumpsSplitter(Splitter):
    """ A class for splitting MUMPS text into functional blocks to prompt
        with for transcoding.
    """

    # Consider labels to delimit subroutines. Labels (and only labels) start on
    #  column 1
    # subroutine_start_pattern: str = re.compile(rf"((?<!\n)\n(?=[^ \t;$]))")
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
        re.VERBOSE | re.DOTALL)

    # subroutine_start_pattern: str = re.compile(rf"(\s*\n(?={label_pattern}|$)|^\s*(?= [^\s;$]))")

    def __init__(self, model: BaseLanguageModel, max_tokens: int = 4096):
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

        # MUMPS text tends to take about 2/3 the space of Python
        self.max_tokens: int = int(max_tokens * 2 / 5)

    def _set_identifiers(self, root: CodeBlock, path: Path):
        stack = [root]
        while stack:
            node = stack.pop()
            node.name = f"{path.name}:{node.id}"
            stack.extend(node.children)

    def _get_ast(self, code: str | bytes) -> CodeBlock:
        code = str(code)

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
        prefixes = betweens[:-1]
        suffixes = betweens[1:]

        # split_code = re.split(self.subroutine_start, code)
        #
        # # Subroutines will be captured in the even indices, while the newlines
        # #  preceding each label will be captured in the odd indices.
        # prefixes = split_code[1:-2:2]
        # chunks = split_code[2::2]
        # suffixes = split_code[3::2]

        start_line = 0
        start_byte = 0
        children: List[CodeBlock] = []
        for prefix, chunk, suffix in zip(prefixes, chunks, suffixes):
            start_byte += len(bytes(prefix, "utf-8"))
            start_line += prefix.count("\n")
            end_byte = start_byte + len(bytes(chunk, "utf-8"))
            end_line = start_line + chunk.count("\n")
            end_char = len(chunk) - chunk.rfind('\n') - 1

            # Set the node name to its label; if there is no label (which will
            #  only occur for the first chunk in the file
            label = re.search(r"^(\w+)", chunk)
            name = label.groups(1)[0] if label is not None else "anon"

            children.append(
                CodeBlock(
                    text=chunk,
                    name=name,
                    id=name,
                    start_point=(start_line, 0),
                    end_point=(end_line, end_char),
                    start_byte=start_byte,
                    end_byte=end_byte,
                    prefix=prefix,
                    suffix=suffix,
                    type=NodeType("subroutine"),
                    children=[],
                    complete=True,
                    language=self.language,
                    tokens=self._count_tokens(chunk)
                )
            )
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
            prefix="",
            suffix="",
            type=NodeType("routine"),
            children=children,
            complete=True,
            language=self.language,
            tokens=self._count_tokens(code)
        )
