import re
from collections import defaultdict
from typing import Optional

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.node import NodeType
from janus.language.splitter import Splitter
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


class AlcRegexSplitter(Splitter):
    """A custom regex-based splitter for IBM ALC (ibmhalsm). Unlike most splitters,
    the nodes of the tree will not line up with the source code order in a
    depth-first traversal
    """

    comment_block_pat = r"(?:(?:^[+ ]*(?:\*.*)?\n)*)"
    label_pat = rf"(?:{comment_block_pat}^[+ ]+([^*\s]*) +)"
    label_pat_uncap = rf"(?:{comment_block_pat}^[+ ]+[^*\s]* +)"
    interruption_pat = rf"(?={label_pat_uncap}[CDR]SECT\b|\Z)"

    # The result of control_section_pat.findall() is a list of tuples where the first
    #  element of each tuple is the full CSECT definition, and the second and third
    #  element are the candidate labels (at least one will be an empty string)
    control_section_start_pat = rf"(?:\A(?:{label_pat}START\b)?|{label_pat}[CR]SECT\b)"
    control_section_pat = re.compile(
        rf"({control_section_start_pat}(?:.*\n)*?){interruption_pat}",
        flags=re.MULTILINE,
    )

    # The result of dummy_section_pat.findall() is a list of tuples where the first
    #  element of each tuple is the full DSECT definition, and the second element
    #  is the DSECT label
    dummy_section_start_pat = rf"(?:{label_pat}DSECT)"
    dummy_section_pat = re.compile(
        rf"({dummy_section_start_pat}(?:.*\n)*?){interruption_pat}",
        flags=re.MULTILINE,
    )

    # Define a "separator comment block" as any block comment that includes a
    #  visual separator (i.e. a line with nothing but comment characters and whitespace)
    viz_sep_pat = r"(?:^[+ ]*\*[*=\-# ]*$)"
    viz_sep_block_pat = re.compile(
        rf"({comment_block_pat}?{viz_sep_pat}\n{comment_block_pat})",
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
        )

    def _get_control_sections(self, code) -> dict[str, list[str]]:
        csects = self.control_section_pat.findall(code)

        continuations = defaultdict(list)
        for defn, n1, n2 in csects:
            defn = defn.strip("\n").rstrip()
            if not defn:
                continue
            name = n1 if n1 else n2
            continuations[name].append(defn)
        return continuations

    def _get_dummy_sections(self, code) -> dict[str, list[str]]:
        dsects = self.dummy_section_pat.findall(code)

        continuations = defaultdict(list)
        for defn, name in dsects:
            defn = defn.strip("\n").rstrip()
            if not defn:
                continue
            continuations[name].append(defn)

        return continuations

    def _get_usings(self, code) -> list[str]:
        return list(set(self.using_pat.findall(code)))

    def _set_identifiers(self, root: CodeBlock, name: str):
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
            dsect_data = node.context_tags
        for child in node.children:
            self._add_dsect_context(child, dsect_data)

    def split_string(self, code: str, name: str) -> CodeBlock:
        root = super().split_string(code=code, name=name)
        self._add_usings(root)
        self._add_dsect_context(root)
        return root

    def _get_ast(self, code: str) -> CodeBlock:
        csect_root = self._get_csect_ast(code)
        dsect_root = self._get_dsect_ast(code)

        # Add DSECTs to CSECT root context tags for later retrieval
        dsects = self._get_dummy_sections(code)
        dsects = {name: "\n".join(lst) for name, lst in dsects.items()}
        csect_root.context_tags["dsects"] = dsects

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
            children=[csect_root, dsect_root],
            language=self.language,
            tokens=self._count_tokens(code),
        )

    def _get_csect_ast(self, code: str) -> CodeBlock:
        csects = self._get_control_sections(code)

        affix = "\n"
        affix_bytes = len(bytes(affix, "utf-8"))

        start_line = 0
        start_byte = 0
        children = []
        for name, chunks in csects.items():
            if not name:
                name = "anon-csect"

            # If there's only one chunk in the list, there are no continuation
            #  sections and this node can be flat
            singleton = len(chunks) == 1

            chunk_children = []
            for i, chunk in enumerate(chunks):
                start_byte += affix_bytes
                start_line += 1
                end_byte = start_byte + len(bytes(chunk, "utf-8"))
                end_line = start_line + chunk.count("\n")
                end_char = len(chunk) - chunk.rfind("\n") - 1

                chunk_name = name if singleton else f"{name}[{i}]"
                node_type = NodeType("csect" if singleton else "csect-continuation")
                node = CodeBlock(
                    text=chunk,
                    name=chunk_name,
                    id=chunk_name,
                    start_point=(start_line, 0),
                    end_point=(end_line, end_char),
                    start_byte=start_byte,
                    end_byte=end_byte,
                    affixes=(affix, affix),
                    node_type=node_type,
                    children=[],
                    language=self.language,
                    tokens=self._count_tokens(chunk),
                )
                self._split_on_visual_separators(node)
                chunk_children.append(node)

                start_byte = end_byte
                start_line = end_line

            if singleton:
                children.extend(chunk_children)
                continue

            merged = affix.join(chunks)
            children.append(
                CodeBlock(
                    text=merged,
                    name=name,
                    id=name,
                    start_point=chunk_children[0].start_point,
                    end_point=chunk_children[-1].end_point,
                    start_byte=chunk_children[0].start_byte,
                    end_byte=chunk_children[-1].end_byte,
                    affixes=("", ""),
                    node_type=NodeType("csect"),
                    children=chunk_children,
                    language=self.language,
                    tokens=self._count_tokens(merged),
                )
            )

        code = "\n".join(c.text for c in children)
        return CodeBlock(
            text=code,
            name="csects",
            id="csects",
            start_point=children[0].start_point,
            end_point=children[-1].end_point,
            start_byte=children[0].start_byte,
            end_byte=children[-1].end_byte,
            affixes=("", ""),
            node_type=NodeType("module-csects"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )

    def _get_dsect_ast(self, code: str) -> CodeBlock:
        dsects = self._get_dummy_sections(code)

        affix = "\n"
        affix_bytes = len(bytes(affix, "utf-8"))

        start_line = 0
        start_byte = 0
        children = []
        for name, chunks in dsects.items():
            if not name:
                name = "anon-dsect"

            # If there's only one chunk in the list, there are no continuation
            #  sections and this node can be flat
            singleton = len(chunks) == 1

            chunk_children: list[CodeBlock] = []
            for i, chunk in enumerate(chunks):
                start_byte += affix_bytes
                start_line += 1
                end_byte = start_byte + len(bytes(chunk, "utf-8"))
                end_line = start_line + chunk.count("\n")
                end_char = len(chunk) - chunk.rfind("\n") - 1

                chunk_name = name if singleton else f"{name}[{i}]"
                node_type = NodeType("dsect" if singleton else "dsect-continuation")
                node = CodeBlock(
                    text=chunk,
                    name=chunk_name,
                    id=chunk_name,
                    start_point=(start_line, 0),
                    end_point=(end_line, end_char),
                    start_byte=start_byte,
                    end_byte=end_byte,
                    affixes=(affix, affix),
                    node_type=node_type,
                    children=[],
                    language=self.language,
                    tokens=self._count_tokens(chunk),
                )
                self._split_on_visual_separators(node)
                chunk_children.append(node)

                start_byte = end_byte
                start_line = end_line

            if singleton:
                children.extend(chunk_children)
                continue

            merged = affix.join(chunks)
            children.append(
                CodeBlock(
                    text=merged,
                    name=name,
                    id=name,
                    start_point=chunk_children[0].start_point,
                    end_point=chunk_children[-1].end_point,
                    start_byte=chunk_children[0].start_byte,
                    end_byte=chunk_children[-1].end_byte,
                    affixes=("", ""),
                    node_type=NodeType("dsect"),
                    children=chunk_children,
                    language=self.language,
                    tokens=self._count_tokens(merged),
                )
            )

        code = "\n".join(c.text for c in children)
        return CodeBlock(
            text=code,
            name="dsects",
            id="dsects",
            start_point=children[0].start_point,
            end_point=children[-1].end_point,
            start_byte=children[0].start_byte,
            end_byte=children[-1].end_byte,
            affixes=("", ""),
            node_type=NodeType("module-dsects"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )

    def _split_on_visual_separators(self, node: CodeBlock):
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

        start_byte = node.start_byte
        start_line, start_char = node.start_point

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
        for i, (prefix, block) in enumerate(chunks):
            chunk = prefix + block
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
                    affixes=("", ""),
                    node_type=NodeType(f"{node.node_type}-chunk"),
                    language=self.language,
                    tokens=self._count_tokens(chunk),
                )
            )
            start_byte = end_byte
            start_line = end_line
            start_char = 0
