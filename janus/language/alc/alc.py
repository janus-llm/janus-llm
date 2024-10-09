import re
from typing import Optional

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.node import NodeType
from janus.language.treesitter import TreeSitterSplitter
from janus.llm.models_info import JanusModel
from janus.utils.logger import create_logger

log = create_logger(__name__)


class AlcCombiner(Combiner):
    """A class that combines code blocks into ALC files."""

    def __init__(self) -> None:
        """Initialize a AlcCombiner instance."""
        super().__init__("ibmhlasm")


class AlcSplitter(TreeSitterSplitter):
    """A class for splitting ALC code into functional blocks to prompt
    with for transcoding.
    """

    def __init__(
        self,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        prune_unprotected: bool = False,
    ):
        """Initialize a AlcSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="ibmhlasm",
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
        )

    def _get_ast(self, code: str) -> CodeBlock:
        root = super()._get_ast(code)

        # Current treesitter implementation does not nest csects and dsects
        # The loop below nests nodes following csect/dsect instructions into
        #  the children of that instruction
        sect_types = {"csect_instruction", "dsect_instruction"}
        queue: list[CodeBlock] = [root]
        while queue:
            block = queue.pop(0)

            # Search this children for csects and dsects. Create a list of groups
            #  where each group is a csect or dsect, starting with the csect/dsect
            #  instruction and containing all the subsequent nodes up until the
            #  next csect or dsect instruction
            sects: list[list[CodeBlock]] = [[]]
            for c in sorted(block.children):
                if c.node_type == "csect_instruction":
                    c.context_tags["alc_section"] = "CSECT"
                    sects.append([c])
                elif c.node_type == "dsect_instruction":
                    c.context_tags["alc_section"] = "DSECT"
                    sects.append([c])
                else:
                    sects[-1].append(c)

            sects = [s for s in sects if s]

            # Restructure the tree, making the head of each group the parent
            #  of all the remaining nodes in that group
            if len(sects) > 1:
                block.children = []
                for sect in sects:
                    if sect[0].node_type in sect_types:
                        sect_node = self.merge_nodes(sect)
                        sect_node.children = sect
                        sect_node.node_type = NodeType(str(sect[0].node_type)[:5])
                        block.children.append(sect_node)
                    else:
                        block.children.extend(sect)

            # Push the children onto the queue
            queue.extend(block.children)

        return root


class AlcListingSplitter(AlcSplitter):
    """A class for splitting ALC listing code into functional blocks to
    prompt with for transcoding.
    """

    def __init__(
        self,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        prune_unprotected: bool = False,
    ):
        """Initialize a AlcSplitter instance.


        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        # The string to mark the end of the listing header
        self.header_indicator_str: str = (
            "Loc  Object Code    Addr1 Addr2  Stmt   Source Statement"
        )
        # How many characters to trim from the right side to remove the address column
        self.address_column_chars: int = 10
        # The string to mark the end of the left margin
        self.left_margin_indicator_str: str = "Stmt"
        super().__init__(
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
        )

    def split_string(self, code: str, name: str) -> CodeBlock:
        # Override split_string to use processed code and track active usings
        active_usings = self.get_active_usings(code)
        processed_code = self.preproccess_assembly(code)
        root = super().split_string(processed_code, name)
        if active_usings is not None:
            stack = [root]
            while stack:
                block = stack.pop()
                block.context_tags["active_usings"] = active_usings
                stack.extend(block.children)
        return root

    def preproccess_assembly(self, code: str) -> str:
        """Remove non-essential lines from an assembly snippet"""

        lines = code.splitlines()
        lines = self.strip_header_and_left(lines)
        lines = self.strip_addresses(lines)
        return "\n".join(str(line) for line in lines)

    def get_active_usings(self, code: str) -> Optional[str]:
        """Look for 'active usings' in the ALC listing header"""
        lines = code.splitlines()
        for line in lines:
            if "Active Usings:" in line:
                return line.split("Active Usings:")[1]
        return None

    def strip_header_and_left(
        self,
        lines: list[str],
    ) -> list[str]:
        """Remove the header and the left panel from the assembly sample"""

        esd_regex = re.compile(f".*{self.header_indicator_str}.*")

        header_end_index: int = [
            i for i, item in enumerate(lines) if re.search(esd_regex, item)
        ][0]

        left_content_end_column = lines[header_end_index].find(
            self.left_margin_indicator_str
        )
        hori_output_lines = lines[(header_end_index + 1) :]

        left_output_lines = [
            line[left_content_end_column + 5 :] for line in hori_output_lines
        ]
        return left_output_lines

    def strip_addresses(self, lines: list[str]) -> list[str]:
        """Strip the addresses which run down the right side of the assembly snippet"""

        stripped_lines = [line[: -self.address_column_chars] for line in lines]
        return stripped_lines

    def strip_footer(self, lines: list[str]):
        """Strip the footer from the assembly snippet"""
        return NotImplementedError
