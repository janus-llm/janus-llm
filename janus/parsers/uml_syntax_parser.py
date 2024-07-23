import subprocess
from typing import Tuple

from langchain.schema.output_parser import BaseOutputParser

from .code_parser import JanusParser


class UMLSyntaxParser(BaseOutputParser, JanusParser):
    def _get_uml_output(self, file: str) -> Tuple[str, str]:
        res = subprocess.run(
            ["plantuml", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout = res.stdout.decode("utf-8")
        stderr = res.stderr.decode("utf-8")
        return stdout, stderr

    def parse(self, text: str) -> str:
        pass
