import os
import platform
import subprocess  # nosec
import tempfile
from pathlib import Path

import tree_sitter

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.treesitter import TreeSitterSplitter
from janus.llm.models_info import JanusModel
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

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

    def __init__(
        self,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str] = (),
        prune_node_types: tuple[str] = (),
    ):
        """Initialize a BinarySplitter instance.

        Arguments:
            model: The language model to use for the binary code
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="binary",
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
        )

    def _execute_ghidra_script(self, cmd: list[str]) -> str:
        """Start a subprocess for headless ghidra to do the actual decompilation

        Arguments:
            cmd: The command to run as a subprocess

        Returns:
            The Ghidra string output
        """
        # We return Bandit B603 here because we are not using shell=True (the more
        # dangerous option)
        # But I added nosec to the end of the line to make it clear that we are aware of
        # the risk
        output = subprocess.run(
            cmd, check=True, shell=False, capture_output=True
        ).stdout  # nosec
        ghidra_output = output.decode(errors="ignore")
        return ghidra_output

    def _get_decompilation(self, file: str) -> str:
        """Decompile a binary file.

        Arguments:
            file: The file to decompile.

        Returns:
            The decompilation as a str of C psuedocode.
        """
        GHIDRA_PATH: str = os.getenv("GHIDRA_INSTALL_PATH")
        if not GHIDRA_PATH:
            log.error(
                "Decompilation failed, the GHIDRA_INSTALL_PATH environment variable is "
                "not set. Follow the Ghidra installation instructions here: "
                "https://ghidra-sre.org/InstallationGuide.html, then run `export "
                "GHIDRA_INSTALL_PATH='<path_to_top_level_ghidra_folder>'`"
            )
        script: str = str(
            Path(GHIDRA_PATH).expanduser().resolve() / "support" / "analyzeHeadless"
        )

        if not Path(script).exists():
            log.error(
                f"Decompilation failed, the Ghidra script {script} does not exist. "
                "Please check that the GHIDRA_INSTALL_PATH environment variable is "
                "set correctly."
            )
            raise FileNotFoundError(f"Could not find Ghidra script {script}")

        fd, temp_decomp_file = tempfile.mkstemp()
        command = (
            script,
            ".",
            "tmp",
            "-readOnly",
            "-import",
            file,
            "-scriptPath",
            ".",
            "-postScript",
            f"{Path(__file__).parent}/reveng/decompile_script.py",
            temp_decomp_file,
        )

        self._execute_ghidra_script(command)
        with open(temp_decomp_file) as f:
            decompilation = f.read()

        os.close(fd)
        # Delete the temporary file if it happens to exist
        tmp_path = Path(temp_decomp_file)
        if tmp_path.exists():
            tmp_path.unlink()

        return decompilation

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        path = Path(file)
        code = self._get_decompilation(file)

        root = self._get_ast(code)
        self._set_identifiers(root, path.name)
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
        lang_dir = tree_sitter_dir / "tree-sitter-c"

        if not lang_dir.exists():
            github_url = LANGUAGES["c"]["url"]
            if github_url is None:
                message = "Tree-sitter does not support c yet."
                log.error(message)
                raise ValueError(message)
            self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(str(so_file), [str(lang_dir)])
