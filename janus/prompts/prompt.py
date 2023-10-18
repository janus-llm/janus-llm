import json
from pathlib import Path
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
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

JSON_OUTPUT = ["evaluate"]

# Directory containing Janus prompt template directories and files
JANUS_PROMPT_TEMPLATES_DIR = Path(__file__).parent / "templates"

# Filenames expected to be found within the above directory
SYSTEM_PROMPT_TEMPLATE_FILENAME = "system.txt"
HUMAN_PROMPT_TEMPLATE_FILENAME = "human.txt"
PROMPT_VARIABLES_FILENAME = "variables.json"


class PromptEngine:
    """A class defining prompting schemes for the LLM."""

    def __init__(
        self,
        source_language: str,
        target_language: str,
        target_version: str,
        prompt_template: str,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            source_language: The language to translate from
            target_language: The language to translate to
            target_version: The version of the target language
            prompt_template: The name of the Janus prompt template directory to use.
                Can be one of "simple", "document", "document_inline", or "requirements",
                or a path to a custom directory containing system.txt and human.txt files.
        """
        # Build base prompt from provided template name
        template_path = self.get_prompt_template_path(prompt_template)
        self._template_path = template_path
        self._template_name = prompt_template
        system_prompt_path = SystemMessagePromptTemplate.from_template(
            (template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME).read_text()
        )
        human_prompt_path = HumanMessagePromptTemplate.from_template(
            (template_path / HUMAN_PROMPT_TEMPLATE_FILENAME).read_text()
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [system_prompt_path, human_prompt_path]
        )

        # Define variables to be passed in to the prompt formatter
        source_language = source_language.lower()
        target_language = target_language.lower()
        self.variables = dict(
            SOURCE_LANGUAGE=source_language.lower(),
            TARGET_LANGUAGE=target_language.lower(),
            TARGET_LANGUAGE_VERSION=str(target_version),
            FILE_SUFFIX=LANGUAGES[source_language]["suffix"],
            SOURCE_CODE_EXAMPLE=LANGUAGES[source_language]["example"],
            TARGET_CODE_EXAMPLE=LANGUAGES[target_language]["example"],
        )
        variables_path = template_path / PROMPT_VARIABLES_FILENAME
        if variables_path.exists():
            self.variables.update(json.loads(variables_path.read_text()))

    def create(self, code: CodeBlock) -> List[BaseMessage]:
        """Convert a code block to a Chat GPT prompt.

        Arguments:
            code: The code block to convert.

        Returns:
            The converted prompt as a list of messages.
        """
        return self.prompt.format_prompt(
            SOURCE_CODE=code.text,
            **self.variables,
        ).to_messages()

    @staticmethod
    def get_prompt_template_path(template_name: str) -> Path:
        """Raises an exception if the specified prompt template path
        is not a directory containing system.txt and human.txt files.

        Arguments:
            template_name: The name of the Janus prompt template directory to use.
                Can be one of "simple", "document", "document_inline", or "requirements",
                or a path to a custom directory containing system.txt and human.txt files.
        """
        template_path = JANUS_PROMPT_TEMPLATES_DIR / template_name
        try:
            PromptEngine._verify_prompt_template_path(template_path)
        except ValueError:
            # Possible that the specified directory is a custom path
            template_path = Path(template_name).expanduser().resolve()
            PromptEngine._verify_prompt_template_path(template_path)
        return template_path

    @staticmethod
    def _verify_prompt_template_path(template_path: Path) -> None:
        """Check for existence of Janus prompt template directory and necessary files

        Arguments:
            template_path: The path to the Janus prompt template directory.

        Raises:
            ValueError: If the specified prompt template directory does not exist,
                is not a directory, or is missing a system.txt or human.txt file.
        """
        if not template_path.exists():
            raise ValueError(
                f"Specified prompt template directory {template_path} does not exist"
            )
        if not template_path.is_dir():
            raise ValueError(
                f"Specified prompt template directory {template_path} is not a directory."
            )
        if not (template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME).exists():
            raise ValueError(
                f"Specified prompt template directory {template_path} is "
                f"missing a {SYSTEM_PROMPT_TEMPLATE_FILENAME}"
            )
        if not (template_path / HUMAN_PROMPT_TEMPLATE_FILENAME).exists():
            raise ValueError(
                f"Specified prompt template directory {template_path} is "
                f"missing a {HUMAN_PROMPT_TEMPLATE_FILENAME}"
            )
