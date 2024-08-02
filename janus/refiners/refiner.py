from janus.llm.models_info import MODEL_PROMPT_ENGINES


class Refiner:
    def refine(self, original_prompt, original_output, errors, **kwargs):
        """
        Creates a new prompt based on feedback from original results
        Arguments:
            original_prompt: original prompt used to produce output
            original_output: origial output of llm
            errors: list of errors detected by parser
        """
        raise NotImplementedError


class BasicRefiner:
    def __init__(
        self,
        prompt_name,
        model_name,
    ):
        self._prompt_name = prompt_name
        self._model_name = model_name

    def refine(self, original_prompt, original_output, errors, **kwargs):
        prompt_engine = MODEL_PROMPT_ENGINES[self._model_name](
            prompt_template=self._prompt_name,
            original_prompt=original_prompt,
            original_output=original_output,
            errors=errors,
        )
        return prompt_engine.prompt
