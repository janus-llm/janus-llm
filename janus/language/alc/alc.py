import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.node import NodeType
from janus.language.splitter import EmptyTreeError, Splitter
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
        skip_merge: bool = False,
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
            skip_merge=skip_merge,
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
                    node_type = sect[0].node_type
                    if node_type in sect_types:
                        if len(sect) == 1:
                            # Don't make a node its own child
                            sect_node = sect[0]
                        else:
                            sect_node = self.merge_nodes(sect)
                            sect_node.children = sect
                        sect_node.node_type = NodeType(str(node_type)[:5])
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


@dataclass
class Section:
    name: str
    definition: str
    start: int
    end: int
    type: str


class AlcRegexSplitter(Splitter):
    """A custom regex-based splitter for IBM ALC (ibmhalsm). Unlike most splitters,
    the nodes of the tree will not line up with the source code order in a
    depth-first traversal
    """

    comment_block_pat = r"(?:(?:^[+ ]*(?:\*.*)?\n)*)"
    label_pat = rf"(?:{comment_block_pat}^[+ ]*([^*\s]*) +)"
    label_pat_uncap = rf"(?:{comment_block_pat}^[+ ]*[^*\s]* +)"
    interruption_pat = rf"(?={label_pat_uncap}[CDR]SECT\b|\Z)"

    # The result of control_section_pat.findall() is a list of tuples where the first
    #  element of each tuple is the full CSECT definition, and the second and third
    #  element are the candidate labels (at least one will be an empty string)
    control_section_start_pat = (
        rf"(?:\A{label_pat}START\b|\A(?!{interruption_pat})|{label_pat}[CR]SECT\b)"
    )
    control_section_pat = re.compile(
        rf"({control_section_start_pat}(?:.*\n)*?.*){interruption_pat}",
        flags=re.MULTILINE,
    )

    # The result of dummy_section_pat.findall() is a list of tuples where the first
    #  element of each tuple is the full DSECT definition, and the second element
    #  is the DSECT label
    dummy_section_start_pat = rf"(?:{label_pat}DSECT)"
    dummy_section_pat = re.compile(
        rf"({dummy_section_start_pat}(?:.*\n)*?.*){interruption_pat}",
        flags=re.MULTILINE,
    )

    # Define a "separator comment block" as any block comment that includes a
    #  visual separator (i.e. a line with nothing but comment characters and whitespace)
    viz_sep_pat = r"(?:^[+ ]*\*[*=\-# ]*\n)"
    viz_sep_block_pat = re.compile(
        rf"({comment_block_pat}{viz_sep_pat}{comment_block_pat})",
        flags=re.MULTILINE,
    )

    using_pat = re.compile(
        r"^[^*\n]{1,15} USING +([\w\-]+)[,\n]",
        flags=re.MULTILINE,
    )

    def __init__(
        self,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        skip_merge: bool = False,
        protected_node_types: tuple[str] = ("csect",),
        prune_node_types: tuple[str] = (),
        prune_unprotected: bool = False,
    ):
        super().__init__(
            language="ibmhlasm",
            model=model,
            max_tokens=max_tokens,
            skip_merge=skip_merge,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
            recalc_border_indices=False,
        )

    def _get_control_sections(self, code) -> dict[str, list[Section]]:
        continuations = defaultdict(list)
        for match in self.control_section_pat.finditer(code):
            sect = Section(
                name=match.group(2) or match.group(3) or "anon-csect",
                definition=match.group(1),
                start=match.start(1),
                end=match.end(1),
                type="csect",
            )
            if not sect.definition.strip():
                continue
            continuations[sect.name].append(sect)
        return continuations

    def _get_dummy_sections(self, code) -> dict[str, list[Section]]:
        continuations = defaultdict(list)
        for match in self.dummy_section_pat.finditer(code):
            sect = Section(
                name=match.group(2) or "anon-dsect",
                definition=match.group(1),
                start=match.start(1),
                end=match.end(1),
                type="dsect",
            )
            continuations[sect.name].append(sect)
        return continuations

    def _get_usings(self, code) -> list[str]:
        return list(set(self.using_pat.findall(code)))

    def _set_identifiers(self, root: CodeBlock, name: str):
        # Setting the node ID is handled in `_split_on_visual_separators` and
        # `_code_block_from_section`.
        return

    def _add_usings(self, root: CodeBlock) -> None:
        """Add USINGS context tags to CSECT nodes to inform retrieval"""
        stack = [root]
        while stack:
            node = stack.pop()
            if node.text is not None and "usings" not in node.context_tags:
                node.context_tags["usings"] = self._get_usings(node.text)
            stack.extend(node.children)

    def _add_dsect_context(self, node: CodeBlock, dsect_data=None) -> None:
        """Recursively add DSECT context to CSECT nodes, for later retrieval"""
        if dsect_data is not None:
            node.context_tags["dsects"] = dsect_data
        elif "dsects" in node.context_tags:
            dsect_data = node.context_tags["dsects"]
        for child in node.children:
            self._add_dsect_context(child, dsect_data)

    def split_string(self, code: str, name: str) -> CodeBlock:
        root = super().split_string(code=code, name=name)
        self._add_usings(root)
        self._add_dsect_context(root)
        return root

    def _get_ast(self, code: str) -> CodeBlock:
        csect_root = self._get_sect_ast(code, "csect")
        dsect_root = self._get_sect_ast(code, "dsect")

        if csect_root is not None:
            # Add DSECTs to CSECT root context tags for later retrieval
            csect_root.context_tags["dsects"] = {}
            if dsect_root is not None:
                csect_root.context_tags["dsects"] = {
                    node.name: node.text for node in dsect_root.children
                }

        children = [c for c in [csect_root, dsect_root] if c is not None]
        if not children:
            raise EmptyTreeError("No sections in source module")
        return CodeBlock(
            text=code,
            name="root",
            id="root",
            start_point=(0, 0),
            end_point=(code.count("\n"), len(code) - code.rfind("\n") - 1),
            start_byte=0,
            end_byte=len(bytes(code, "utf-8")),
            affixes=("", ""),
            node_type=NodeType("module"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )

    def _code_block_from_section(
        self,
        code: str,
        sect: Section,
        continuation_idx: int = -1,
    ) -> CodeBlock:
        if continuation_idx >= 0:
            sect.name = f"{sect.name}[{continuation_idx}]"
            sect.type = f"{sect.type}-continuation"

        # Trim leading and trailing newlines, update boundary indices to match
        lpad = len(sect.definition) - len(sect.definition.lstrip("\n"))
        rpad = len(sect.definition) - len(sect.definition.rstrip("\n"))
        sect.start += lpad
        sect.end -= rpad
        sect.definition = sect.definition.strip("\n")

        # Also count the newlines before and after the match
        head = code[: sect.start]
        sect.definition = code[sect.start : sect.end]
        tail = code[sect.end :]
        lpad = len(head) - len(head.rstrip("\n"))
        rpad = len(tail) - len(tail.lstrip("\n"))

        # Get boundary location data
        start_byte = len(bytes(head, "utf-8"))
        start_line = head.count("\n")
        start_char = sect.start - head.rfind("\n") - 1
        end_byte = start_byte + len(bytes(sect.definition, "utf-8"))
        end_line = start_line + sect.definition.count("\n")
        end_char = len(sect.definition) - sect.definition.rfind("\n") - 1

        node = CodeBlock(
            text=sect.definition,
            name=sect.name,
            id=sect.name,
            start_point=(start_line, start_char),
            end_point=(end_line, end_char),
            start_byte=start_byte,
            end_byte=end_byte,
            affixes=("\n" * lpad, "\n" * rpad),
            node_type=NodeType(sect.type),
            children=[],
            language=self.language,
            tokens=self._count_tokens(sect.definition),
        )
        self._split_on_visual_separators(node, code)
        return node

    def _get_sect_ast(self, code: str, type: str) -> CodeBlock | None:
        if type == "dsect":
            sect_dict = self._get_dummy_sections(code)
        elif type == "csect":
            sect_dict = self._get_control_sections(code)
        else:
            raise ValueError(f"Expected type to be 'dsect' or 'csect', got {type}")

        if not sect_dict:
            return None

        children = []
        for name, sects in sect_dict.items():
            # If there's only one chunk in the list, there are no continuation
            #  sections and this node can be flat
            if len(sects) == 1:
                children.append(self._code_block_from_section(code=code, sect=sects[0]))
                continue

            chunk_children: list[CodeBlock] = [
                self._code_block_from_section(code=code, sect=sect, continuation_idx=i)
                for i, sect in enumerate(sects)
            ]

            chunk = "\n".join(c.text or "" for c in chunk_children)
            children.append(
                CodeBlock(
                    text=chunk,
                    name=name,
                    id=name,
                    start_point=chunk_children[0].start_point,
                    end_point=chunk_children[-1].end_point,
                    start_byte=chunk_children[0].start_byte,
                    end_byte=chunk_children[-1].end_byte,
                    node_type=NodeType(type),
                    children=chunk_children,
                    language=self.language,
                    tokens=self._count_tokens(chunk),
                )
            )

        code = "\n".join(c.text for c in children)
        return CodeBlock(
            text=code,
            name=f"{type}s",
            id=f"{type}s",
            start_point=children[0].start_point,
            end_point=children[-1].end_point,
            start_byte=children[0].start_byte,
            end_byte=children[-1].end_byte,
            node_type=NodeType(f"module-{type}s"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )

    def _split_on_visual_separators(self, node: CodeBlock, code: str):
        if node.text is None:
            return

        # Because the pattern is captured, the comment blocks will appear between
        #  each chunk in the split list (e.g. [chunk, sep, chunk, sep, chunk])
        # If the string begins or ends with a comment block, the list will begin
        #  or end with an empty string
        split_text = list(self.viz_sep_block_pat.split(node.text))

        # If the string has no separator, or just one at the beginning/end, do not split
        if len(split_text) == 1:
            return
        elif len(split_text) <= 3 and not (split_text[0] and split_text[-1]):
            return

        # If there's an empty string at the head of the list, the code starts
        #  with a separator comment block. Remove the head to start with the
        #  first comment separator
        # If the string *doesn't* start with an empty string, then the first
        #  chunk doesn't have a separator comment in front of it; add one
        if not split_text[0]:
            split_text.pop(0)
        else:
            split_text.insert(0, "")

        # If there's an empty string at the end of the list, the code ends with
        #  a separator comment block. Merge it into the penultimate block
        if not split_text[-1]:
            split_text[-3:] = ["".join(split_text[-3:])]

        chunks = zip(split_text[::2], split_text[1::2])
        start_idx = len(bytes(code, "utf-8")[: node.start_byte].decode("utf-8"))
        for i, (prefix, block) in enumerate(chunks):
            chunk = prefix + block

            # Trim leading and trailing newlines, update boundary indices to match
            lpad = len(chunk) - len(chunk.lstrip("\n"))
            rpad = len(chunk) - len(chunk.rstrip("\n"))
            chunk = chunk.strip("\n")
            start_idx += lpad
            end_idx = start_idx + len(chunk)

            # Also count the newlines before and after the match
            head = code[:start_idx]
            chunk = code[start_idx:end_idx]
            tail = code[end_idx:]
            full_lpad = len(head) - len(head.rstrip("\n"))
            full_rpad = len(tail) - len(tail.lstrip("\n"))

            # Get boundary location data
            start_byte = len(bytes(head, "utf-8"))
            start_line = head.count("\n")
            start_char = start_idx - head.rfind("\n") - 1
            end_byte = start_byte + len(bytes(chunk, "utf-8"))
            end_line = start_line + chunk.count("\n")
            end_char = len(chunk) - chunk.rfind("\n") - 1

            node.children.append(
                CodeBlock(
                    text=chunk,
                    name=f"{node.name}_chunk[{i}]",
                    id=f"{node.id}_chunk[{i}]",
                    start_byte=start_byte,
                    start_point=(start_line, start_char),
                    end_byte=end_byte,
                    end_point=(end_line, end_char),
                    affixes=("\n" * full_lpad, "\n" * full_rpad),
                    node_type=NodeType(f"{node.node_type}-chunk"),
                    language=self.language,
                    tokens=self._count_tokens(chunk),
                )
            )

            # Only increment start index by original rpad, to start at beginning
            #  of next prefix (which may start with newlines)
            start_idx += len(chunk) + rpad

    def _split_into_lines(self, node: CodeBlock):
        super()._split_into_lines(node)
        # Because the leaf nodes are not in traversal order, must migrate
        #  affixes to the leaves so they're not lost
        node.trickle_down_affixes()
