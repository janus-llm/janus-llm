from dataclasses import dataclass
from typing import List

from langchain import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import ChatMessagePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.messages import BaseMessage

from ..language.block import CodeBlock
from ..utils.enums import LANGUAGES
from ..utils.logger import create_logger

log = create_logger(__name__)


# Prompt names (self.template_map keys) that should output text,
# regardless of the `output-lang` argument.
TEXT_OUTPUT = ["document", "requirements"]
# Prompt names (self.template_map keys) that should output the
# same language as the input, regardless of the `output-lang` argument.
SAME_OUTPUT = ["document_inline"]


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
        model_name: str,
        source_language: str,
        target_language: str,
        target_version: str,
        prompt_template_name: str,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            model: The LLM to use for translation.
            source_language: The language to translate from
            target_language: The language to translate to
            target_version: The version of the target language
            prompt_template_name: The name of the prompt template to use. Can be one of
                "simple", "document", "document_inline", or "requirements".
        """
        self.model = model
        self.model_name = model_name
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = str(target_version)
        self.prompt_template: ChatPromptTemplate
        self.document_inline_prompt_template: ChatPromptTemplate
        self.document_prompt_template: ChatPromptTemplate
        self.requirements_prompt_template: ChatPromptTemplate
        self._create_prompt_template()
        self.prompt_template_name = prompt_template_name
        self.example_source_code = LANGUAGES[self.source_language]["example"]
        self.example_target_code = LANGUAGES[self.target_language]["example"]
        self.suffix = LANGUAGES[self.source_language]["suffix"]

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
        prompt = self.template_map[self.prompt_template_name].format_messages(
            SOURCE_LANGUAGE=self.source_language,
            TARGET_LANGUAGE=self.target_language,
            TARGET_LANGUAGE_VERSION=self.target_version,
            SOURCE_CODE=code.code,
            FILE_SUFFIX=self.suffix,
            EXAMPLE_SOURCE_CODE=self.example_source_code,
            EXAMPLE_TARGET_CODE=self.example_target_code,
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
        if "gpt" in self.model_name:
            messages = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Your purpose is to convert {SOURCE_LANGUAGE} {FILE_SUFFIX} code "
                        "into runnable {TARGET_LANGUAGE} code ({TARGET_LANGUAGE} version "
                        "{TARGET_LANGUAGE_VERSION})"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Do not include anything around the resultant code. "
                        "Only report back the code itself in between triple backticks."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If the given code is incomplete, "
                        "assume it is translated elsewhere. "
                        "Translate it anyway."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If the given code is missing variable definitions, "
                        "assume they are assigned elsewhere. "
                        "Translate it anyway."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Give an attempt even if it is incomplete."
                        "If the code only consists of comments, assume the code that is "
                        "represented by that comment is translated elsewhere. "
                        "Translate it anyway."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If the code has comments, keep ALL of them"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If the code only consists of ONLY comments, "
                        "assume the code that is "
                        "represented by those comments is translated elsewhere. "
                        "Translate it anyway."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please convert the following {SOURCE_LANGUAGE} {FILE_SUFFIX} "
                        "code found in between triple backticks "
                        "and is in string format into "
                        "{TARGET_LANGUAGE} code. "
                        "If the given code is incomplete, assume it "
                        "is translated elsewhere. If the given code is missing variable "
                        "definitions, assume they are assigned elsewhere. If there are "
                        "incomplete statements that haven't been closed out, "
                        "assume they are "
                        "closed out in other translations. "
                        "If it only consists of comments, "
                        "assume the code that is represented "
                        "by that comment is translated "
                        "elsewhere. If it only consists of ONLY comments, "
                        "assume the code that "
                        "Some more things to remember: "
                        "(1) follow standard styling practice for "
                        "the target language, "
                        "(2) make sure the language is typed correctly. "
                        "Make sure your result also fits within three backticks."
                        "\n\n```{SOURCE_CODE}```"
                    ),
                ),
            ]
            messages_document_inline = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Please add inline comments to the {SOURCE_LANGUAGE} file"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please provide docstrings and inline comments for this code"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code code found in between triple backticks and is "
                        "in string format.\n\n```{SOURCE_CODE}```"
                        "Make sure your result also fits within three backticks."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Keep all source code in the output."
                    ),
                ),
            ]
            messages_document = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Please document the {SOURCE_LANGUAGE} "
                        "file in a simplified manner"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code\n\n{SOURCE_CODE}"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "For any variable that is defined outside "
                        "of that function please explain"
                        " that variable."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "For any abbreviations, please define them"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please add a description of the top which "
                        "includes details why this file"
                        " was created or modified"
                    ),
                ),
            ]
            messages_requirements = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Your purpose is to understand a source code file "
                        "and generate a software requirements specification "
                        "document for it."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please convert the following code into software "
                        "requirements that can replicate its functionality."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "In addition, describe the capabilities and "
                        "limitations of the functionality, as well as how "
                        "to test the functionality."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please output English sentences in the style of an "
                        "IEEE Software Requirements Specification document"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If you think any section of the code is difficult to "
                        "understand or has uncertain requirements, state what it is."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code\n\n{SOURCE_CODE}"
                    ),
                ),
            ]
        else:
            messages = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "You are an AI named Llama in a converstion with a human named user. "
                        "Your purpose is to implement {SOURCE_LANGUAGE} {FILE_SUFFIX} code "
                        "in {TARGET_LANGUAGE} ({TARGET_LANGUAGE} version "
                        "{TARGET_LANGUAGE_VERSION})"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Implement the following {SOURCE_LANGUAGE} {FILE_SUFFIX} "
                        "code found in between triple backticks "
                        "in {TARGET_LANGUAGE} code. "
                        "If the given code is incomplete, assume it "
                        "is implemented elsewhere. If the given code is missing variable "
                        "definitions, assume they are assigned elsewhere. If there are "
                        "incomplete statements that haven't been closed out, "
                        "assume they are closed out elsewhere. "
                        "If it only consists of "
                        "comments, "
                        "just implement the comments. If the program contains "
                        "comments, keep ALL of them. "
                        "If there are any issues, implement the code anyway. "
                        "Some more things to remember: "
                        "(1) follow standard styling practice for "
                        "the target language, "
                        "(2) make sure the language is typed correctly. "
                        "You must provide your result within three backticks "
                        "\n\n```{EXAMPLE_SOURCE_CODE}```"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="Llama",
                    prompt=PromptTemplate.from_template(
                        "```{TARGET_LANGUAGE} {EXAMPLE_TARGET_CODE}```"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Good, now please implement the following {SOURCE_LANGUAGE} {FILE_SUFFIX} "
                        "code found in between triple backticks "
                        "in {TARGET_LANGUAGE} code. "
                        "If the given code is incomplete, assume it "
                        "is implemented elsewhere. If the given code is missing variable "
                        "definitions, assume they are assigned elsewhere. If there are "
                        "incomplete statements that haven't been closed out, "
                        "assume they are closed out elsewhere. "
                        "If it only consists of "
                        "comments, "
                        "just implement the comments. If the program contains "
                        "comments, keep ALL of them. "
                        "If there are any issues, implement the code anyway. "
                        "Some more things to remember: "
                        "(1) follow standard styling practice for "
                        "the target language, "
                        "(2) make sure the language is typed correctly. "
                        "You must provide your result within three backticks "
                        "\n\n```{SOURCE_CODE}```"
                    ),
                ),
            ]
            messages_document_inline = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Please add inline comments to the {SOURCE_LANGUAGE} file"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please provide docstrings and inline comments for this code"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code code found in between triple backticks and is "
                        "in string format.\n\n```{SOURCE_CODE}```"
                        "Make sure your result also fits within three backticks."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Keep all source code in the output."
                    ),
                ),
            ]
            messages_document = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Please document the {SOURCE_LANGUAGE} "
                        "file in a simplified manner"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code\n\n{SOURCE_CODE}"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "For any variable that is defined outside "
                        "of that function please explain"
                        " that variable."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "For any abbreviations, please define them"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please add a description of the top "
                        "which includes details why this file"
                        " was created or modified"
                    ),
                ),
            ]
            messages_requirements = [
                ChatMessagePromptTemplate(
                    role="system",
                    prompt=PromptTemplate.from_template(
                        "Your purpose is to understand a source code file "
                        "and generate a software requirements specification "
                        "document for it."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please convert the following code into software "
                        "requirements that can replicate its functionality."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "In addition, describe the capabilities and "
                        "limitations of the functionality, as well as how "
                        "to test the functionality."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Please output English sentences in the style of an "
                        "IEEE Software Requirements Specification document"
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "If you think any section of the code is difficult to "
                        "understand or has uncertain requirements, state what it is."
                    ),
                ),
                ChatMessagePromptTemplate(
                    role="user",
                    prompt=PromptTemplate.from_template(
                        "Here is the code\n\n{SOURCE_CODE}"
                    ),
                ),
            ]
        self.prompt_template = ChatPromptTemplate.from_messages(messages)
        self.document_inline_prompt_template = ChatPromptTemplate.from_messages(
            messages_document_inline
        )
        self.document_prompt_template = ChatPromptTemplate.from_messages(
            messages_document
        )
        self.requirements_prompt_template = ChatPromptTemplate.from_messages(
            messages_requirements
        )

        self.template_map = {
            "simple": self.prompt_template,
            "document_inline": self.document_inline_prompt_template,
            "document": self.document_prompt_template,
            "requirements": self.requirements_prompt_template,
        }
