import re

from langchain.schema.output_parser import BaseOutputParser


class CodeParser(BaseOutputParser):
    target_language: str

    def parse(self, text: str) -> str:
        pattern = rf"```[^\S\r\n]*(?:{self.target_language}[^\S\r\n]*)?\n?(.*?)\n*```"
        try:
            response = re.search(pattern, text, re.DOTALL).group(1)
        except Exception:
            raise ValueError("Code is not between ```")
        return response
