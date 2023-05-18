from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

import tiktoken

from ..language.block import CodeBlock
from ..llm.openai import MODEL_TYPES
from ..utils.language import LANGUAGE_SUFFIXES
from ..utils.logger import create_logger

log = create_logger(__name__)


@dataclass
class Prompt:
    """The prompt for a code block.

    Attributes:
        prompt: The prompt for the code block.
        code: The `CodeBlock`.
        tokens: The total tokens in the prompt.
    """

    prompt: List[Dict[str, str]]
    code: CodeBlock
    tokens: int


@dataclass
class PromptTemplate:
    """The prompt template to use for a code block.

    Attributes:
        simple: The simple prompt template.
    """

    simple: Tuple[Dict[str, str]] = (
        {
            "role": "system",
            "content": (
                "Your purpose is to convert <SOURCE LANGUAGE> <FILE SUFFIX> code "
                "into runnable <TARGET LANGUAGE> code (<TARGET LANGUAGE> version "
                "<TARGET LANGUAGE VERSION>)"
            ),
        },
        {
            "role": "user",
            "content": (
                "Please convert the following <SOURCE LANGUAGE> <FILE SUFFIX> code found "
                "in between triple backticks and is in string format into useable "
                "<TARGET LANGUAGE> code. \n\n```<SOURCE CODE>```"
            ),
        },
    )


class PromptEngine:
    """A class defining prompting schemes for the LLM."""

    def __init__(
        self,
        model: str,
        source_language: str,
        target_language: str,
        target_version: str,
        prompt_template: str,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            model: The LLM to use for translation.
        """
        self.model = model.lower()
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = str(target_version)
        self.prompt_template = prompt_template.lower()
        self._check_prompt_templates()

    def create(self, code: CodeBlock) -> Prompt:
        """Create a prompt for the given code block.

        Arguments:
            code: The `CodeBlock` to create a prompt for.

        Returns:
            A `Prompt` instance.
        """
        if MODEL_TYPES[self.model] == "chat-gpt":
            prompt = self._code_to_chat_prompt(code)
        else:
            log.error(f"Model type '{self.model}' not implemented")
            raise NotImplementedError(f"Model type '{self.model}' not implemented")

        return Prompt(prompt, code, self._count_tokens(prompt))

    def _code_to_chat_prompt(self, code: CodeBlock) -> List[Dict[str, str]]:
        """Convert a code block to a Chat GPT prompt.

        Arguments:
            code: The code block to convert.

        Returns:
            The converted prompt.
        """
        prompt: List[Dict[str, str]] = []

        for message in self.prompt_template:
            log.debug(f"Message: {message}")
            message["content"] = message["content"].replace(
                "<SOURCE LANGUAGE>", self.source_language
            )
            message["content"] = message["content"].replace(
                "<TARGET LANGUAGE>", self.target_language
            )
            message["content"] = message["content"].replace(
                "<TARGET LANGUAGE VERSION>", self.target_version
            )
            message["content"] = message["content"].replace("<SOURCE CODE>", code.code)
            message["content"] = message["content"].replace(
                "<FILE SUFFIX>", LANGUAGE_SUFFIXES[code.language]
            )
            prompt.append(message)

        return prompt

    def _str_to_chat_prompt(self, prompt: str) -> List[Dict[str, str]]:
        """Convert a string to a Chat GPT prompt.

        Arguments:
            prompt: The prompt to convert.

        Returns:
            The converted prompt.
        """
        return [
            {"role": "user", "content": prompt},
        ]

    def _count_tokens(self, prompt: str | List[Dict[str, str]]) -> int:
        """Count the number of tokens in the given prompt.

        Arguments:
            prompt: The prompt to count the tokens in.

        Returns:
            The number of tokens in the prompt.
        """
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
            log.debug(
                f"Using default encoding for token counting with model '{self.model}'"
            )

        if isinstance(prompt, str):
            messages = self._str_to_chat_prompt(prompt)
        elif isinstance(prompt, list):
            messages = prompt
        else:
            log.error(f"Prompt type '{type(prompt)}' not recognized")
            raise ValueError(f"Prompt type '{type(prompt)}' not recognized")

        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        log.debug(f"Number of tokens in prompt: {num_tokens}")
        return num_tokens

    def _check_prompt_templates(self) -> None:
        """Check that the prompt template is valid."""
        valid_prompt_templates = asdict(PromptTemplate()).keys()
        if self.prompt_template not in valid_prompt_templates:
            log.error(
                f"Prompt template '{self.prompt_template}' not recognized. "
                f"Valid prompt templates are {valid_prompt_templates}"
            )
            raise ValueError(
                f"Prompt template '{self.prompt_template}' not recognized. "
                f"Valid prompt templates are {valid_prompt_templates}"
            )
        self.prompt_template = asdict(PromptTemplate())[self.prompt_template]
