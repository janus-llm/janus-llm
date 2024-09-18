from typing import Any

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable

from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


retry_prompt_text = """Prompt:
--------------
{prompt}
--------------
Completion:
--------------
{completion}
--------------

Above, the Completion did not satisfy the constraints given in the Prompt.
Error:
--------------
{error}
--------------

Please try again. Please only respond with an answer that satisfies the
constraints laid out in the Prompt:"""


retry_prompt = PromptTemplate.from_template(retry_prompt_text)


class JanusRefiner(JanusParser):
    parser: JanusParser
    max_retries: int

    def parse_runnable(self, input: dict[str, Any]) -> Any:
        return self.parse_completion(**input)

    def parse_completion(self, completion: str, **kwargs) -> Any:
        return self.parser.parse(completion)

    def parse(self, text: str) -> str:
        raise NotImplementedError


class FixParserExceptions(JanusRefiner, RetryWithErrorOutputParser):
    def __init__(self, llm: BaseLanguageModel, parser: JanusParser, max_retries: int):
        chain = retry_prompt | llm | StrOutputParser()
        RetryWithErrorOutputParser.__init__(
            self, parser=parser, retry_chain=chain, max_retries=max_retries
        )

    def parse_completion(
        self, completion: str, prompt_value: PromptValue, **kwargs
    ) -> Any:
        return self.parse_with_prompt(completion, prompt_value=prompt_value)


reflection_prompt_text = """Task Description:
--------------
{prompt}
--------------
Completion:
--------------
{completion}
--------------

You are a programmer reviewing code documentation. Generate critique and
suggestions for the provided completion, including requests for added
detail, corrections of factual errors, improved style, etc.
Do not rewrite the output yourself, only provide critique that can be acted on.
Provide no further commentary or questions other than your feedback.

If the provided documentation is to your satisfaction, respond with "LGTM".
It is important that "LGTM" be returned on its own with no further commentary.
"""

revision_prompt_text = """Task Description:
--------------
{prompt}
--------------
Completion:
--------------
{completion}
--------------
Feedback:
--------------
{reflection}
--------------

Given the above documentation task, completion, and feedback, improve the
completion by incorporating the feedback. Respond only with the revised output,
following the format indicated in the original task description, do not provide
any additional feedback or questions about the critique.
"""

reflection_prompt = PromptTemplate.from_template(reflection_prompt_text)
revision_prompt = PromptTemplate.from_template(revision_prompt_text)


class ReflectionRefiner(JanusRefiner):
    reflection_chain: RunnableSerializable
    revision_chain: RunnableSerializable

    def __init__(self, llm: BaseLanguageModel, parser: JanusParser, max_retries: int):
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
        for _ in range(self.max_retries):
            reflection = self.reflection_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                )
            )
            log.info(f"Reflection:\n{reflection}")
            if reflection.strip() == "LGTM":
                return self.parser.parse(completion)
            completion = self.revision_chain.invoke(
                dict(
                    prompt=prompt_value.to_string(),
                    completion=completion,
                    reflection=reflection,
                )
            )
            log.info(f"Revision:\n{completion}")

        return self.parser.parse(completion)
