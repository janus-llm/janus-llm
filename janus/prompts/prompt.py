import json
from abc import ABC, abstractmethod
from pathlib import Path

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.prompts import PromptTemplate

from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


# Prompt names (self.template_map keys) that should output text,
# regardless of the `output-lang` argument.
TEXT_OUTPUT = []

# Prompt names (self.template_map keys) that should output the
# same language as the input, regardless of the `output-lang` argument.
SAME_OUTPUT = ["document_inline"]

JSON_OUTPUT = ["evaluate", "document", "document_madlibs", "requirements"]

# Directory containing Janus prompt template directories and files
JANUS_PROMPT_TEMPLATES_DIR = Path(__file__).parent / "templates"

# Filenames expected to be found within the above directory
SYSTEM_PROMPT_TEMPLATE_FILENAME = "system.txt"
HUMAN_PROMPT_TEMPLATE_FILENAME = "human.txt"
PROMPT_VARIABLES_FILENAME = "variables.json"


retry_with_output_prompt_text = """Instructions:
--------------
{instructions}
--------------
Completion:
--------------
{completion}
--------------

Above, the Completion did not satisfy the constraints given in the Instructions.
Error:
--------------
{error}
--------------

Please try again. Please only respond with an answer that satisfies the
constraints laid out in the Instructions:"""


retry_with_error_and_output_prompt_text = """Prompt:
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


retry_with_output_prompt = PromptTemplate.from_template(retry_with_output_prompt_text)
retry_with_error_and_output_prompt = PromptTemplate.from_template(
    retry_with_error_and_output_prompt_text
)


class PromptEngine(ABC):
    """A class defining prompting schemes for the LLM."""

    def __init__(
        self,
        source_language: str,
        prompt_template: str,
        target_language: str | None = None,
        target_version: str | None = None,
    ) -> None:
        """Initialize a PromptEngine instance.

        Arguments:
            source_language: The language to translate from
            target_language: The language to translate to
            target_version: The version of the target language
            prompt_template: The name of the Janus prompt template directory to use.
                Can be one of "simple", "document", "document_inline", "pseudocode", or
                "requirements", or a path to a custom directory containing system.txt and
                human.txt files.
        """
        # Build base prompt from provided template name
        template_path = self.get_prompt_template_path(prompt_template)
        self._template_path = template_path
        self._template_name = prompt_template
        self.prompt = self.load_prompt_template(template_path)

        # Define variables to be passed in to the prompt formatter
        source_language = source_language.lower()
        self.variables = dict(
            SOURCE_LANGUAGE=source_language,
            FILE_SUFFIX=LANGUAGES[source_language]["suffix"],
            SOURCE_CODE_EXAMPLE=LANGUAGES[source_language]["example"],
        )
        if target_language is not None:
            target_language = target_language.lower()
            self.variables.update(
                TARGET_LANGUAGE=target_language,
                TARGET_CODE_EXAMPLE=LANGUAGES[target_language]["example"],
            )
            self.variables.update(TARGET_LANGUAGE_VERSION=str(target_version))
        variables_path = template_path / PROMPT_VARIABLES_FILENAME
        if variables_path.exists():
            self.variables.update(json.loads(variables_path.read_text()))
        self.prompt = self.prompt.partial(**self.variables)

    @abstractmethod
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        pass

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


class ChatGptPromptEngine(PromptEngine):
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        system_prompt_path = template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME
        system_prompt = system_prompt_path.read_text()
        system_message = SystemMessagePromptTemplate.from_template(system_prompt)

        human_prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        human_prompt = human_prompt_path.read_text()
        human_message = HumanMessagePromptTemplate.from_template(human_prompt)
        return ChatPromptTemplate.from_messages([system_message, human_message])


class ClaudePromptEngine(PromptEngine):
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        prompt = prompt_path.read_text()
        return PromptTemplate.from_template(f"Human: {prompt}\n\nAssistant: ")


class TitanPromptEngine(PromptEngine):
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        prompt = prompt_path.read_text()
        return PromptTemplate.from_template(f"User: {prompt}\n\nAssistant: ")


class Llama2PromptEngine(PromptEngine):
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        system_prompt_path = template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME
        system_prompt = system_prompt_path.read_text()

        human_prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        human_prompt = human_prompt_path.read_text()

        return PromptTemplate.from_template(
            f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{human_prompt} [/INST]"
        )


class Llama3PromptEngine(PromptEngine):
    # see https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3
    #            /#special-tokens-used-with-meta-llama-3
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        system_prompt_path = template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME
        system_prompt = system_prompt_path.read_text()

        human_prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        human_prompt = human_prompt_path.read_text()

        return PromptTemplate.from_template(
            f"<|begin_of_text|>"
            f"<|start_header_id|>"
            f"system"
            f"<|end_header_id|>"
            f"\n\n{system_prompt}"
            f"<|eot_id|>"
            f"<|start_header_id|>"
            f"user"
            f"<|end_header_id|>"
            f"\n\n{human_prompt}"
            f"<|eot_id|>"
            f"<|start_header_id|>"
            f"assistant"
            f"<|end_header_id|>"
            f"\n\n"
        )


class CoherePromptEngine(PromptEngine):
    # see https://docs.cohere.com/docs/prompting-command-r
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        system_prompt_path = template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME
        system_prompt = system_prompt_path.read_text()

        human_prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        human_prompt = human_prompt_path.read_text()

        return PromptTemplate.from_template(
            f"<BOS_TOKEN>"
            f"<|START_OF_TURN_TOKEN|>"
            f"<|SYSTEM_TOKEN|>"
            f"{system_prompt}"
            f"<|END_OF_TURN_TOKEN|>"
            f"<|START_OF_TURN_TOKEN|>"
            f"<|USER_TOKEN|>"
            f"{human_prompt}"
            f"<|END_OF_TURN_TOKEN|>"
        )


class MistralPromptEngine(PromptEngine):
    def load_prompt_template(self, template_path: Path) -> ChatPromptTemplate:
        system_prompt_path = template_path / SYSTEM_PROMPT_TEMPLATE_FILENAME
        system_prompt = system_prompt_path.read_text()

        human_prompt_path = template_path / HUMAN_PROMPT_TEMPLATE_FILENAME
        human_prompt = human_prompt_path.read_text()

        return PromptTemplate.from_template(
            f"<s>[INST] {system_prompt} [/INST] </s>[INST] {human_prompt}  [/INST]"
        )
