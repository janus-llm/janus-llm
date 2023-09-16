import re

from langchain.schema.output_parser import BaseOutputParser


class CodeParser(BaseOutputParser):
    target_language: str

    def parse(self, text: str) -> str:
        pattern = rf"```[^\S\r\n]*(?:{self.target_language}[^\S\r\n]*)?\n?(.*?)\n*```"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise ValueError("Code not between ```")
        return code.group(1)
