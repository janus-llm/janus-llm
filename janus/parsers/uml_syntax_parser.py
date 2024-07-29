import re
import subprocess
from pathlib import Path
from typing import List, Tuple

from langchain_core.exceptions import OutputParserException

from .code_parser import CodeParser


class UMLSyntaxParser(CodeParser):
    def _get_uml_output(self, file: str) -> Tuple[str, str]:
        res = subprocess.run(
            ["plantuml", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout = res.stdout.decode("utf-8")
        stderr = res.stderr.decode("utf-8")
        return stdout, stderr

    def _get_errs(self, s: str) -> List[str]:
        return [x.group() for x in re.finditer(r"Error (.*)\n", s)]

    def parse(self, text: str) -> str:
        text = super().parse(text)
        temp_file_path = Path.home().expanduser() / Path(".janus/tmp.txt")
        with open(temp_file_path, "w") as f:
            f.write(text)
        uml_std_out, uml_std_err = self._get_uml_output(temp_file_path)
        uml_errs = self._get_errs(uml_std_out) + self._get_errs(uml_std_err)
        if len(uml_errs) > 0:
            raise OutputParserException(
                "Error: Received UML Errors:\n" + "\n".join(uml_errs)
            )
        return text
