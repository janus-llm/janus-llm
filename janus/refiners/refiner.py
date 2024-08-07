from typing import Dict, Tuple

from langchain_core.prompts import ChatPromptTemplate

from janus.llm.models_info import MODEL_PROMPT_ENGINES


class Refiner:
    def refine(
        self, original_prompt: str, original_output: str, errors: str, **kwargs
    ) -> Tuple[ChatPromptTemplate, Dict[str, str]]:
        """
        Creates a new prompt based on feedback from original results
        Arguments:
            original_prompt: original prompt used to produce output
            original_output: origial output of llm
            errors: list of errors detected by parser
        Return: Tuple of new prompt and prompt arguments
        """
        raise NotImplementedError


class BasicRefiner(Refiner):
    def __init__(
        self,
        prompt_name,
        model_name,
        source_language,
    ):
        """
        Basic refiner, asks llm to fix output of previous prompt given errors
        Arguments:
            prompt_name: refinement prompt name to use
            model_name: name of llm to use
            source_language: source_langauge to use
        """
        self._prompt_name = prompt_name
        self._model_name = model_name
        self._source_language = source_language

    def refine(self, original_prompt: str, original_output: str, errors: str, **kwargs):
        prompt_engine = MODEL_PROMPT_ENGINES[self._model_name](
            prompt_template=self._prompt_name,
            source_language=self._source_language,
        )
        prompt_arguments = {
            "ORIGINAL_PROMPT": original_prompt,
            "OUTPUT": original_output,
            "ERRORS": errors,
        }
        return prompt_engine.prompt, prompt_arguments
