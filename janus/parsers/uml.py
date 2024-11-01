import re
import subprocess  # nosec
from pathlib import Path
from tempfile import NamedTemporaryFile

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage

from janus.parsers.code_parser import CodeParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class UMLSyntaxParser(CodeParser):
    def _check_plantuml(self, text: str) -> None:
        # Leading newlines can break the parser, remove them
        text = text.replace("\\n", "\n").strip()

        # Write the text to a temporary file (automatically deleted)
        file = NamedTemporaryFile()
        fname = file.name
        with open(fname, "w") as fin:
            fin.write(text)

        try:
            plantuml_path = Path.home().expanduser() / ".janus/lib/plantuml.jar"
            # NOTE: running subprocess with shell=False, added nosec to
            # label that we know risk exists
            res = subprocess.run(
                ["java", "-jar", plantuml_path, fname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )  # nosec
            stdout = res.stdout.decode("utf-8")
            stderr = res.stderr.decode("utf-8")
        except FileNotFoundError:
            err_txt = (
                "Plant UML executable not found. Either choose a different parser"
                " or install with `bash scripts/install_plantuml.sh`. Java and"
                " graphviz are dependencies for the tool, they must also be installed."
            )
            log.error(err_txt)
            raise Exception(err_txt)

        # Check for bad outputs, raise OutputParserExceptions if so
        if "Error" in stderr or "Error" in stdout:
            err_txt = "Recieved UML parsing error(s)."

            line_nos = self._get_error_lines(stderr) + self._get_error_lines(stdout)
            lines = text.split("\n")
            for i in line_nos:
                i0 = max(0, i - 3)
                i1 = min(len(lines) - 1, i + 2)
                err_lines = [
                    f"> {lines[j]}" if j == i - 1 else f"  {lines[j]}"
                    for j in range(i0, i1)
                ]
                if i0:
                    err_lines.insert(0, "  ...")
                if i1 < (len(lines) - 1):
                    err_lines.append("  ...")

                err_txt += f"\nError located at line {i} must be fixed:\n"
                err_txt += "\n".join(err_lines)
            log.warning(err_txt)
            raise OutputParserException(err_txt)

        if "Warning" in stdout or "Warning" in stderr:
            err_txt = "Recieved UML parsing warning (often due to missing PLANTUML)."
            if stderr:
                err_txt += f"\nSTDERR:\n```\n{stderr.strip()}\n```\n"
            if stdout:
                err_txt += f"\nSTDOUT:\n```\n{stdout.strip()}\n```\n"

            log.warning(err_txt)
            raise OutputParserException(err_txt)

    def _get_error_lines(self, s: str) -> list[int]:
        return [int(x.group(1)) for x in re.finditer(r"Error line (\d+) in file:", s)]

    def _get_warns(self, s: str) -> list[str]:
        return [x.group() for x in re.finditer(r"Warning: (.*)\n", s)]

    def parse(self, text: str | BaseMessage) -> str:
        text = super().parse(text)
        self._check_plantuml(text)
        return text
