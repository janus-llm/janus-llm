import re
from typing import Any

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
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


class SimpleRetry(JanusRefiner):
    max_retries: int
    retry_chain: RunnableSerializable

    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
    ):
        retry_chain = llm | StrOutputParser()
        super().__init__(
            retry_chain=retry_chain,
            parser=parser,
            max_retries=max_retries,
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        for retry_number in range(self.max_retries):
            try:
                return self.parser.parse(completion)
            except OutputParserException:
                completion = self.retry_chain.invoke(prompt_value)

        return self.parser.parse(completion)


class FixParserExceptions(JanusRefiner, RetryWithErrorOutputParser):
    def __init__(self, llm: JanusModel, parser: JanusParser, max_retries: int):
        retry_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
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
    reflection_prompt_name: str

    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
        prompt_template_name: str = "refinement/reflection",
    ):
        reflection_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template=prompt_template_name,
        ).prompt
        revision_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template="refinement/revision",
        ).prompt

        reflection_chain = reflection_prompt | llm | StrOutputParser()
        revision_chain = revision_prompt | llm | StrOutputParser()
        super().__init__(
            reflection_prompt_name=prompt_template_name,
            reflection_chain=reflection_chain,
            revision_chain=revision_chain,
            parser=parser,
            max_retries=max_retries,
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        log.debug(f"Reflection Prompt: {self.reflection_prompt_name}")
        for retry_number in range(self.max_retries):
            reflection = self.reflection_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                )
            )
            if re.search(r"\bLGTM\b", reflection) is not None:
                return self.parser.parse(completion)
            if not retry_number:
                log.debug(f"Completion:\n{completion}")
            log.debug(f"Reflection:\n{reflection}")
            completion = self.revision_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                    reflection=reflection,
                )
            )
            log.debug(f"Revision:\n{completion}")

        return self.parser.parse(completion)


class RequirementsReflectionRefiner(JanusRefiner):
    """
    This requirements-specific refiner is intended to address a common issue with
    requirements reflection, where over the course of several reflection loops,
    requirements lists grow increasingly verbose, eventually becoming too wordy
    to be useful. To reduce this, this refiner interlaces an additional reflection
    -> revision loop which de-duplicates requirements.
    """

    max_retries: int
    reflection_chain: RunnableSerializable
    revision_chain: RunnableSerializable
    reflect_duplication_chain: RunnableSerializable
    revise_duplication_chain: RunnableSerializable
    reflection_prompt_name: str

    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
        prompt_template_name: str = "refinement/reflection/incose",
    ):
        # Main reflection loop
        reflection_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template="refinement/reflection/incose",
        ).prompt
        revision_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template="refinement/revision/incose",
        ).prompt
        # De-duplication loop
        reflect_duplication_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template="refinement/reflection/incose_deduplicate",
        ).prompt
        revise_duplication_prompt = MODEL_PROMPT_ENGINES[llm.short_model_id](
            source_language="text",
            prompt_template="refinement/revision/incose_deduplicate",
        ).prompt

        reflection_chain = reflection_prompt | llm | StrOutputParser()
        revision_chain = revision_prompt | llm | StrOutputParser()
        reflect_duplication_chain = reflect_duplication_prompt | llm | StrOutputParser()
        revise_duplication_chain = revise_duplication_prompt | llm | StrOutputParser()
        super().__init__(
            reflection_prompt_name=prompt_template_name,
            reflection_chain=reflection_chain,
            revision_chain=revision_chain,
            reflect_duplication_chain=reflect_duplication_chain,
            revise_duplication_chain=revise_duplication_chain,
            parser=parser,
            max_retries=max_retries,
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        log.debug(f"Reflection Prompt: {self.reflection_prompt_name}")
        if isinstance(completion, AIMessage):
            completion = completion.content
        for retry_number in range(self.max_retries):
            # First, check if the generated requirements are redundant or too specific
            duplication_reflection = self.reflect_duplication_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                )
            )
            if re.search(r"\bLGTM\b", duplication_reflection) is not None:
                log.debug(
                    "No de-duplication suggested in reflection, "
                    "passing to next reflection step"
                )
            else:
                completion = self.revise_duplication_chain.invoke(
                    dict(
                        prompt=prompt_value.to_string(),
                        completion=completion,
                        reflection=duplication_reflection,
                    )
                )

            # Once we're happy with the results or trimmed them down,
            # continue with the typical reflection process,
            # except with specific INCOSE-focused prompts
            reflection = self.reflection_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                )
            )
            if re.search(r"\bLGTM\b", reflection) is not None:
                return self.parser.parse(completion)
            if not retry_number:
                log.debug(f"Completion:\n{completion}")
            completion = self.revision_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                    reflection=reflection,
                )
            )

        return self.parser.parse(completion)


class HallucinationRefiner(ReflectionRefiner):
    def __init__(self, **kwargs):
        super().__init__(
            prompt_template_name="refinement/hallucination",
            **kwargs,
        )
