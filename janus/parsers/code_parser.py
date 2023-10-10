import re

from langchain.schema.output_parser import BaseOutputParser


class CodeParser(BaseOutputParser):
    target_language: str

    def parse(self, text: str) -> str:
        pattern = rf"```[^\S\r\n]*(?:{self.target_language}[^\S\r\n]*)?\n?(.*?)\n*```"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise ValueError("Code not find code between triple backticks")
        return code.group(1)


class FormattedTextParser(CodeParser):
    target_language = "formatted_text"

    def parse(self, text: str) -> str:
        string = r"\"\w+\""
        json_value = rf"(?:{string}|-?[\d.]+)"
        json_line = rf"\s*{string} *: *{json_value},?\s*"
        pattern = "({" + rf"(?:{json_line})+" + "})"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise ValueError("Could not find JSON output")
        return code.group(1)
