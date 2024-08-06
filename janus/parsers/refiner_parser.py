from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException


class RefinerParser(BaseOutputParser):
    def __init__(
        self,
        llm,
        parser,
        initial_prompt,
        refiner,
        max_retries,
    ):
        self._llm = llm
        self._parser = parser
        self._initial_prompt = initial_prompt
        self._refiner = refiner
        self._max_retries = max_retries

    def parse(self, text: str) -> str:
        last_prompt = self._initial_prompt
        for _ in range(self._max_retries):
            try:
                self._parser.parse(text)
            except OutputParserException as oe:
                err = str(oe)
                new_prompt, prompt_arguments = self._refiner.refine(
                    last_prompt, text, err
                )
                new_chain = new_prompt | self._llm
                text = new_chain.invoke(prompt_arguments)
                last_prompt = new_prompt.format(prompt_arguments)
        raise OutputParserException(
            f"Error: unable to correct output after {self._max_retries} attempts"
        )
