import os
import subprocess
import platform
from pathlib import Path
from typing import List
from typing import Optional

import tree_sitter
from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..combine import Combiner
from ..node import NodeType
from ..treesitter import TreeSitterSplitter

log = create_logger(__name__)


class BinaryCombiner(Combiner):
    """A class that combines code blocks into binary files."""

    def __init__(self) -> None:
        """Initialize a BinaryCombiner instance."""
        super().__init__("binary")


class BinarySplitter(TreeSitterSplitter):
    """A class for splitting binary code into functional blocks to prompt
    with for transcoding.
    """

    def __init__(self, model: BaseLanguageModel, max_tokens: int = 4096):
        """Initialize a BinarySplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="binary",
            model=model,
            max_tokens=max_tokens,
            use_placeholders=False,
        )

    def execute_ghidra_script(self, cmd: str) -> str:
        output = subprocess.run(cmd, check=True, shell=True, capture_output=True).stdout
        ghidra_output = output.decode(errors="ignore")
        return ghidra_output

    def get_decompilation(self, file: str, output_path: str) -> str:
        GHIDRA_PATH: str = "~/dev/ghidra_10.3.3_PUBLIC/"
        script: str = GHIDRA_PATH + "support" + "/" + "analyzeHeadless"

        # TODO!
        os.system("rm -rf tmp*")
        command = (
            f"{script} . tmp -readOnly -import {file} -scriptPath . -postScript"
            f" {Path(__file__).parent}/rev_eng/decompile_script.py {os.path.join(output_path, 'decompilation')}"
        )
        print(output_path)
        print(command)

        self.execute_ghidra_script(command)
        with open(os.path.join(output_path, 'decompilation'), "r") as f:
        # with open(os.path.join(output_path, 'decompilation_fixup'), "r") as f:
        # with open(os.path.join(output_path, 'smaz.c'), "r") as f:
            decompilation = f.read()

        print(f"Decompilation: {decompilation}")
        return decompilation

    def get_disassembly(self, file: str, output_path: str) -> str:
        GHIDRA_PATH: str = "~/dev/ghidra_10.3.3_PUBLIC/"
        script: str = GHIDRA_PATH + "support" + "/" + "analyzeHeadless"

        os.system("rm -rf tmp*")
        command = (
            f"{script} . tmp -readOnly -import {file} -scriptPath . -postScript"
            f" ~/dev/janus/rellm/rellm/rev_eng/ghidra_utils/disassemble_script.py {os.path.join(output_path, 'disassembly')}"
        )
        print(command)

        self.execute_ghidra_script(command)
        disassembly = ""
        with open(os.path.join(output_path, 'disassembly'), "r") as f:
            lines = f.readlines()
            for line in lines:
                disassembly += line[56:]

        return disassembly

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        path = Path(file)
        code = self.get_decompilation(file, ".")

        root = self._get_ast(code)
        self._set_identifiers(root, path)
        self._segment_leaves(root)
        self._merge_tree(root)

        return root

    def _load_parser(self) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.
        """
        # Get the directory to store the file in from environment (or default)
        build_dir: Path = Path.home() / ".janus/tree-sitter/build-files"
        if (custom_dir := os.environ.get("TREE_SITTER_BUILD_DIR")) is not None:
            build_dir = Path(custom_dir)

        # Locate the .so file, generate the file if necessary
        platform_str = f"{platform.system()}_{platform.processor()}"
        so_file = build_dir / f"{self.language}_parser_{platform_str}.so"
        if not so_file.exists():
            log.warning(
                f"Could not load {so_file}, building one for {platform.system()} "
                f"system, with {platform.processor()} processor"
            )
            self._create_parser(so_file)

        # string required for Windows, as 'WindowsPath' is not iterable
        so_file = str(so_file)

        # Load the parser using the generated .so file
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        self.parser.set_language(tree_sitter.Language(so_file, "c"))

    def _create_parser(self, so_file: Path | str) -> None:
        """Create the parser for the given language.

        Arguments:
            so_file: The path to the so file for the language.
        """
        # Store the library in the `build` directory
        tree_sitter_dir = Path.home() / ".tree-sitter"
        tree_sitter_dir.mkdir(exist_ok=True)
        lang_dir = tree_sitter_dir / f"tree-sitter-c"

        if not lang_dir.exists():
            github_url = LANGUAGES["c"]["url"]
            if github_url is None:
                message = f"Tree-sitter does not support c yet."
                log.error(message)
                raise ValueError(message)
            self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(str(so_file), [str(lang_dir)])

