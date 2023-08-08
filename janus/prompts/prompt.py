from dataclasses import dataclass
from typing import List
from ..language.block import CodeBlock
from ..utils.logger import create_logger
from langchain.prompts import ChatPromptTemplate, 
from langchain.prompts.chat import ChatMessagePromptTemplate
from langchain.schema.messages import BaseMessage
from langchain.schema.language_model import BaseLanguageModel
from langchain import PromptTemplate

log = create_logger(__name__)

@dataclass
class Prompt:
    """The prompt for a code block.

    Attributes:
        prompt: The prompt for the code block.
        code: The `CodeBlock`.
        tokens: The total tokens in the prompt.
    """

    prompt: List[BaseMessage]
    code: CodeBlock
    tokens: int


class PromptEngine:
    """A class defining prompting schemes for the LLM."""

    def __init__(
        self,
        model: BaseLanguageModel,
        source_language: str,
        target_language: str,
        target_version: str,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            model: The LLM to use for translation.
            source_language: The language to translate from
            target_language: The language to translate to
            target_version: The version of the target language
        """
        self.model = model
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = str(target_version)
        self.message_templates = message_templates
        self.prompt_template: ChatPromptTemplate
        self._create_prompt_template()

    def create(self, code: CodeBlock) -> Prompt:
        """Create a prompt for the given code block.

        Arguments:
            code: The `CodeBlock` to create a prompt for.

        Returns:
            A `Prompt` instance.
        """
        prompt = self._code_to_chat_prompt(code)

        return Prompt(prompt, code, self._count_tokens(prompt))


    def _code_to_chat_prompt(self, code: CodeBlock) -> List[BaseMessage]:
        """Convert a code block to a Chat GPT prompt.

        Arguments:
            code: The code block to convert.

        Returns:
            The converted prompt.
        """
        prompt = self.prompt_template.format_messages(
            SOURCE_LANGUAGE=self.source_language,
            TARGET_LANGUAGE=self.target_language,
            TARGET_LANGUAGE_VERSION=self.target_version,
            SOURCE_CODE=code.code,
            FILE_SUFFIX=code.language,
        )

        return prompt

    def _count_tokens(self, prompt: str | List[BaseMessage]) -> int:
        """Count the number of tokens in the given prompt.

        Arguments:
            prompt: The prompt to count the tokens in.

        Returns:
            The number of tokens in the prompt.
        """
        if isinstance(prompt, list):
            return self.model.get_num_tokens_from_messages(prompt)
        return self.model.get_num_tokens(prompt)
    
    def _create_prompt_template(self) -> None:
        """Create the prompt template to be used for generating messages"""
        messages = [
            ChatMessagePromptTemplate(
                role="system",
                prompt=PromptTemplate.from_template(
                            "Your purpose is to convert {SOURCE_LANGUAGE} {FILE_SUFFIX} code "
                            "into runnable {TARGET_LANGUAGE} code ({TARGET_LANGUAGE} version "
                            "{TARGET_LANGUAGE_VERSION})"
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "Do not include anything around the resultant code. Only report back the "
                            "code itself in between triple backticks."
                            )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "If the given code is incomplete, assume it is translated elsewhere. "
                            "Translate it anyway."
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "If the given code is missing variable definitions, assume they are "
                            "assigned elsewhere. "
                            "Translate it anyway."
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "Give an attempt even if it is incomplete."
                            "If the code only consists of comments, assume the code that is "
                            "represented by that comment is translated elsewhere. "
                            "Translate it anyway."
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "If the code has comments, keep ALL of them"
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "If the code only consists of ONLY comments, assume the code that is "
                            "represented by those comments is translated elsewhere. "
                            "Translate it anyway."
                )
            ),
            ChatMessagePromptTemplate(
                role="human",
                prompt=PromptTemplate.from_template(
                            "Please convert the following {SOURCE_LANGUAGE} {FILE_SUFFIX} code found "
                            "in between triple backticks and is in string format into "
                            "{TARGET_LANGUAGE} code. If the given code is incomplete, assume it "
                            "is translated elsewhere. If the given code is missing variable "
                            "definitions, assume they are assigned elsewhere. If there are "
                            "incomplete statements that haven't been closed out, assume they are "
                            "closed out in other translations. If it only consists of comments, "
                            "assume the code that is represented by that comment is translated "
                            "elsewhere. If it only consists of ONLY comments, assume the code that "
                            "Some more things to remember: (1) follow standard styling practice for "
                            "the target language, (2) make sure the language is typed correctly. "
                            "Make sure your result also fits within three backticks."
                            "\n\n```{SOURCE_CODE}```"
                )
            )
        ]
        self.prompt_template = ChatPromptTemplate.from_messages(messages)
