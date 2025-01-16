from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableSerializable

from janus.llm.models_info import MODEL_PROMPT_ENGINES, JanusModel
from janus.parsers.parser import JanusParser
from janus.refiners.refiner import JanusRefiner


class FormatRefiner(JanusRefiner):
    format_chain: RunnableSerializable

    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
        prompt_template_name: str,
    ):
        format_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template=prompt_template_name,
        ).prompt
        format_chain = format_prompt | llm | StrOutputParser()
        super().__init__(
            format_chain=format_chain, parser=parser, max_retries=max_retries
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        completion = self.format_chain.invoke(
            dict(completion=completion, prompt=prompt_value.to_string())
        )
        return self.parser.parse(completion)


class CodeFormatRefiner(FormatRefiner):
    def __init__(self, llm: JanusModel, parser: JanusParser, max_retries: int):
        super().__init__(llm, parser, max_retries, "refinement/format/code_format")


class RequirementsFormatRefiner(FormatRefiner):
    def __init__(self, llm: JanusModel, parser: JanusParser, max_retries: int):
        super().__init__(
            llm, parser, max_retries, "refinement/format/requirements_format"
        )
