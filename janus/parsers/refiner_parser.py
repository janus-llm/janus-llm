from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import BaseOutputParser

from janus.refiners.refiner import Refiner


class RefinerParser(BaseOutputParser):
    """Parser for performing refinement with a refiner

    Properties:
        llm: the language model to use
        parser: the parser to use for parsing llm output
        initial_prompt: initial prompt used to generate output
        refiner: refiner that gives new subsequent prompts
        max_retires: maximum number of times to attempt refining
    """

    class Config:
        arbitrary_types_allowed = True

    llm: BaseLanguageModel
    parser: BaseOutputParser
    initial_prompt: str
    refiner: Refiner
    max_retries: int

    def parse(self, text: str) -> str:
        """Parses the text using the refiner

        Arguments:
            text: text to parse

        Returns:
            Parsed text
        """
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
