from typing import Any

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableSerializable

from janus.llm.models_info import MODEL_PROMPT_ENGINES, JanusModel
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class JanusRefiner(JanusParser):
    parser: JanusParser

    def parse_runnable(self, input: dict[str, Any]) -> Any:
        return self.parse_completion(**input)

    def parse_completion(self, completion: str, **kwargs) -> Any:
        return self.parser.parse(completion)

    def parse(self, text: str) -> str:
        raise NotImplementedError


class FixParserExceptions(JanusRefiner, RetryWithErrorOutputParser):
    def __init__(self, llm: JanusModel, parser: JanusParser, max_retries: int):
        retry_prompt = MODEL_PROMPT_ENGINES[llm.model_id](
            source_language="text",
            prompt_template="refinement/fix_exceptions",
        ).prompt
        chain = retry_prompt | llm | StrOutputParser()
        RetryWithErrorOutputParser.__init__(
            self, parser=parser, retry_chain=chain, max_retries=max_retries
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        return self.parse_with_prompt(completion, prompt_value=prompt_value)


class ReflectionRefiner(JanusRefiner):
    max_retries: int
    reflection_chain: RunnableSerializable
    revision_chain: RunnableSerializable

    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
        prompt_template_name: str = "refinement/reflection",
    ):
        reflection_prompt = MODEL_PROMPT_ENGINES[llm.model_id](
            source_language="text",
            prompt_template=prompt_template_name,
        ).prompt
        revision_prompt = MODEL_PROMPT_ENGINES[llm.model_id](
            source_language="text",
            prompt_template="refinement/revision",
        ).prompt

        reflection_chain = reflection_prompt | llm | StrOutputParser()
        revision_chain = revision_prompt | llm | StrOutputParser()
        super().__init__(
            reflection_chain=reflection_chain,
            revision_chain=revision_chain,
            parser=parser,
            max_retries=max_retries,
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        for retry_number in range(self.max_retries):
            reflection = self.reflection_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                )
            )
            if reflection.strip() == "LGTM":
                return self.parser.parse(completion)
            if not retry_number:
                log.info(f"Completion:\n{completion}")
            log.info(f"Reflection:\n{reflection}")
            completion = self.revision_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                    reflection=reflection,
                )
            )
            log.info(f"Revision:\n{completion}")

        return self.parser.parse(completion)


class HallucinationRefiner(ReflectionRefiner):
    def __init__(self, **kwargs):
        super().__init__(
            prompt_template_name="refinement/hallucination",
            **kwargs,
        )


REFINERS = dict(
    none=JanusRefiner,
    parser=FixParserExceptions,
    reflection=ReflectionRefiner,
    hallucination=HallucinationRefiner,
)
