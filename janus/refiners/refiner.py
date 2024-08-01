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
    pass
