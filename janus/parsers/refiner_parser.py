from typing import Any

from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException


class RefinerParser(BaseOutputParser):
    llm: Any
    parser: Any
    initial_prompt: Any
    refiner: Any
    max_retries: Any

    def parse(self, text: str) -> str:
        last_prompt = self.initial_prompt
        for _ in range(self.max_retries):
            try:
                return self.parser.parse(text)
            except OutputParserException as oe:
                err = str(oe)
                new_prompt, prompt_arguments = self.refiner.refine(last_prompt, text, err)
                new_chain = new_prompt | self.llm
                text = new_chain.invoke(prompt_arguments)
                last_prompt = new_prompt.format(**prompt_arguments)
        raise OutputParserException(
            f"Error: unable to correct output after {self.max_retries} attempts"
        )
