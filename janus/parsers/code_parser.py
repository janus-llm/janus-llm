import re

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class CodeParser(JanusParser):
    language: str

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        pattern = rf"```[^\S\r\n]*(?:{self.language}[^\S\r\n]*)?\n?(.*?)\n*```"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise JanusParserException(
                text,
                "Code not find code between triple backticks",
            )
        return str(code.group(1))

    def get_format_instructions(self) -> str:
        return "Output must contain text contained within triple backticks (```)"


class IncompleteCodeParser(JanusParser):
    language: str

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        code_start_pattern = rf"^.*?```[^\S\r\n]*(?:{self.language}[^\S\r\n]*)\n"
        if re.search(code_start_pattern, text, flags=re.DOTALL) is None:
            log.info(f"Exception, bad output: {text}")
            raise JanusParserException(
                text,
                f"Code must start with annotated backticks (``` {self.language})"
            )
        code = re.sub(code_start_pattern, "", text, flags=re.DOTALL)

        # If code does not end in triple backticks, it's incomplete; don't strip
        code_end_pattern = r"\n*```.*$"
        if re.search(code_end_pattern, code, flags=re.DOTALL) is None:
            return text
        
        return re.sub(code_end_pattern, "", code, flags=re.DOTALL)

    def strip_head(self, text: str) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        code_start_pattern = rf"^.*?```[^\S\r\n]*(?:{self.language}[^\S\r\n]*)\n"
        return re.sub(code_start_pattern, "", text, flags=re.DOTALL)

    def strip_tail(self, text: str) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        code_start_pattern = rf"^.*?```\s*(?:{self.language}[^\S\r\n]*)\n"
        code_end_pattern = r"\n*```.*?$"

        # If there's no opening ```, then it should be safe to remove any
        #  closing ``` without losing code
        if (m := re.search(code_start_pattern, text, flags=re.DOTALL)) is None:
            return re.sub(code_end_pattern, "", text, flags=re.DOTALL)

        # If there is an opening ```, then we don't want to accidentally delete
        #  all the code in the case of a missing closing ```
        idx = m.span()[1]
        return text[:idx] + re.sub(code_end_pattern, "", text[idx:], flags=re.DOTALL)


    def get_format_instructions(self) -> str:
        return (
            "Code must be contained within triple backticks (```), and should"
            " include the language name after the opening backticks, like so:\n"
            f"``` {self.language}\n<CODE>\n```\n\n"
            "If no closing backticks are found, it is assumed that the code is incomplete"
        )