import re
import subprocess  # nosec
from pathlib import Path
from typing import List, Tuple

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage

from janus.parsers.code_parser import CodeParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class UMLSyntaxParser(CodeParser):
    def _get_uml_output(self, file: Path) -> Tuple[str, str]:
        # NOTE: running subprocess with shell=False, added nosec to label that we know
        # risk exists
        try:
            plantuml_path = Path.home().expanduser() / ".janus/lib/plantuml.jar"
            res = subprocess.run(
                ["java", "-jar", plantuml_path, file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )  # nosec
            stdout = res.stdout.decode("utf-8")
            stderr = res.stderr.decode("utf-8")
        except FileNotFoundError:
            log.warning("Plant UML executable not found, skipping syntax check")
            stdout = ""
            stderr = ""
        return stdout, stderr

    def _get_errs(self, s: str) -> List[str]:
        return [x.group() for x in re.finditer(r"Error (.*)\n", s)]

    def parse(self, text: str | BaseMessage) -> str:
        text = super().parse(text)
        janus_path = Path.home().expanduser() / Path(".janus")
        if not janus_path.exists():
            janus_path.mkdir()
        temp_file_path = janus_path / "tmp.txt"
        with open(temp_file_path, "w") as f:
            f.write(text)
        uml_std_out, uml_std_err = self._get_uml_output(temp_file_path)
        uml_errs = self._get_errs(uml_std_out) + self._get_errs(uml_std_err)
        if len(uml_errs) > 0:
            raise OutputParserException(
                "Error: Received UML Errors:\n" + "\n".join(uml_errs)
            )
        return text
