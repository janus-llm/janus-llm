import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
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

# Directory containing Janus prompt template directories and files
JANUS_PROMPT_TEMPLATES_DIR = Path("janus/prompts/templates")
SYSTEM_PROMPT_TEMPLATE_FILENAME = "system.txt"
HUMAN_PROMPT_TEMPLATE_FILENAME = "human.txt"
PROMPT_VARIABLES_FILENAME = "variables.json"


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
        prompt_template: str,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            model: The LLM to use for translation.
            source_language: The language to translate from
            target_language: The language to translate to
            target_version: The version of the target language
            prompt_template: The name of the Janus prompt template directory to use.
                Can be one of "simple", "document", "document_inline", or "requirements",
                or a path to a custom directory containing system.txt and human.txt files.
        """
        self.model = model
        self.model_name = model_name
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = str(target_version)

        self.prompt_template = prompt_template
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
        prompt, extra_variables = self._load_prompt_template(self.prompt_template)

        messages = prompt.format_prompt(
            SOURCE_LANGUAGE=self.source_language,
            TARGET_LANGUAGE=self.target_language,
            TARGET_LANGUAGE_VERSION=self.target_version,
            SOURCE_CODE=code.code,
            FILE_SUFFIX=self.suffix,
            **extra_variables,
        ).to_messages()

        return messages

    def _verify_prompt_template_dir(self, dir_path: Path) -> None:
        """Raises an exception if the specified prompt template path
        is not a directory containing system.txt and human.txt files.
        """
        if not dir_path.exists():
            raise Exception(
                f"Specified prompt template directory {dir_path} does not exist"
            )
        if not dir_path.is_dir():
            raise Exception(
                f"Specified prompt template directory {dir_path} is not a directory."
            )
        if (
            not (dir_path / SYSTEM_PROMPT_TEMPLATE_FILENAME).exists()
            or not (dir_path / HUMAN_PROMPT_TEMPLATE_FILENAME).exists()
        ):
            raise Exception(
                f"Specified prompt template directory {dir_path} should contain" +
                f"{SYSTEM_PROMPT_TEMPLATE_FILENAME} and" +
                f"{HUMAN_PROMPT_TEMPLATE_FILENAME} files."
            )

    def _load_prompt_template(self, dir_name: str) -> (ChatPromptTemplate, dict):
        """Loads chat prompt templates and variables from directory files."""

        # Check for existence of Janus prompt template directory and necessary files
        template_dir = JANUS_PROMPT_TEMPLATES_DIR / dir_name
        try:
            self._verify_prompt_template_dir(template_dir)
        except Exception:
            # Possible that the specified directory is a custom path
            template_dir = Path(dir_name)
            self._verify_prompt_template_dir(template_dir)

        system_template_filepath = template_dir / SYSTEM_PROMPT_TEMPLATE_FILENAME
        human_template_filepath = template_dir / HUMAN_PROMPT_TEMPLATE_FILENAME

        system_prompt = SystemMessagePromptTemplate.from_template(
            self._load_prompt_template_file(system_template_filepath)
        )
        human_prompt = HumanMessagePromptTemplate.from_template(
            self._load_prompt_template_file(human_template_filepath)
        )

        # Initialize extra template variables to empty dictionary
        prompt_variables = {}
        # If a variables file exists, read into the dictionary
        prompt_variables_filepath = template_dir / PROMPT_VARIABLES_FILENAME
        if prompt_variables_filepath.exists():
            with open(prompt_variables_filepath, "r") as f:
                prompt_variables = json.load(f)

        return (
            ChatPromptTemplate.from_messages([system_prompt, human_prompt]),
            prompt_variables,
        )

    def _load_prompt_template_file(self, filepath: Path) -> str:
        """Read in the specified .txt file as a string.
        File can contain multiple lines but they will be concatenated.

        """
        return filepath.read_text().replace("\n", " ")

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
