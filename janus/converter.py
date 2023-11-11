import functools
from typing import Any

from langchain.schema.language_model import BaseLanguageModel

from .language.combine import Combiner
from .language.mumps import MumpsSplitter
from .language.splitter import Splitter
from .language.treesitter import TreeSitterSplitter
from .parsers.code_parser import PARSER_TYPES, CodeParser, EvaluationParser, JanusParser
from .utils.enums import CUSTOM_SPLITTERS, LANGUAGES
from .utils.logger import create_logger

log = create_logger(__name__)


def run_if_changed(*tracked_vars):
    """Wrapper to skip function calls if the given instance attributes haven't
    been updated. Requires the _changed_attrs set to exist, and the __setattr__
    method to be overridden to track parameter updates in _changed_attrs.
    """

    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            # If there is overlap between the tracked variables and the changed
            #  ones, then call the function as normal
            if self._changed_attrs.intersection(tracked_vars):
                func(self, *args, **kwargs)

        return wrapped

    return wrapper


class Converter:
    """Parent class that converts code into something else.

    Children will determine what the code gets converted into. Whether that's translated
    into another language, into pseudocode, requirements, documentation, etc., or
    converted into embeddings
    """

    def __init__(
        self,
        source_language: str = "fortran",
        parser_type: None | str = None,
    ) -> None:
        """Initialize a Converter instance.

        Arguments:
            source_language: The source programming language.
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are `"code"`, `"text"`, `"eval"`, and `None` (default). If `None`,
                the `Converter` assumes you won't be parsing an output (i.e., adding to an
                embedding DB).
        """
        self._changed_attrs: set = set()

        self._parser_type: None | str
        self._source_language: None | str
        self._source_glob: None | str
        self._parser: None | JanusParser
        self._splitter: None | Splitter
        self._llm: None | BaseLanguageModel

        self._combiner: Combiner = Combiner()

        self.set_parser_type(parser_type=parser_type)
        self.set_source_language(source_language=source_language)

        self._load_parameters()

    def __setattr__(self, key: Any, value: Any) -> None:
        if hasattr(self, "_changed_attrs"):
            if not hasattr(self, key) or getattr(self, key) != value:
                self._changed_attrs.add(key)
        # Avoid infinite recursion
        elif key != "_changed_attrs":
            self._changed_attrs = set()
        super().__setattr__(key, value)

    def _load_parameters(self) -> None:
        self._load_splitter()
        self._load_parser()
        self._changed_attrs.clear()

    def set_source_language(self, source_language: str) -> None:
        """Validate and set the source language.

        The affected objects will not be updated until translate() is called.

        Arguments:
            source_language: The source programming language.
        """
        source_language = source_language.lower()
        if source_language not in LANGUAGES:
            raise ValueError(
                f"Invalid source language: {source_language}. "
                "Valid source languages are found in `janus.utils.enums.LANGUAGES`."
            )

        self._source_glob = f"**/*.{LANGUAGES[source_language]['suffix']}"
        self._source_language = source_language

    def set_parser_type(self, parser_type: str) -> None:
        """Validate and set the parser type.

        The affected objects will not be updated until translate() is called.

        Arguments:
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are "code" (default), "text", and "eval".
        """
        if parser_type not in PARSER_TYPES:
            raise ValueError(
                f'Unsupported parser type "{parser_type}". Valid types: '
                f"{PARSER_TYPES}"
            )
        self._parser_type = parser_type

    @run_if_changed("_source_language", "_max_tokens", "_llm")
    def _load_splitter(self) -> None:
        """Load the splitter according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        if self._source_language in CUSTOM_SPLITTERS:
            if self._source_language == "mumps":
                self.splitter = MumpsSplitter(
                    max_tokens=self._max_tokens,
                    model=self._llm,
                )
        else:
            self.splitter = TreeSitterSplitter(
                language=self._source_language,
                max_tokens=self._max_tokens,
                model=self._llm,
            )

    @run_if_changed("_parser_type", "_target_language")
    def _load_parser(self) -> None:
        """Load the parser according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        if "text" == self._target_language and self._parser_type != "text":
            raise ValueError(
                f"Target language ({self._target_language}) suggests target "
                f"parser should be 'text', but is '{self._parser_type}'"
            )
        if "code" == self._parser_type:
            self.parser = CodeParser(language=self._target_language)
        elif "eval" == self._parser_type:
            self.parser = EvaluationParser(
                expected_keys={"syntax", "style", "completeness", "correctness"}
            )
        elif "text" == self._parser_type:
            self.parser = JanusParser()
        else:
            raise ValueError(
                f"Unsupported parser type: {self._parser_type}. Can be: "
                f"{PARSER_TYPES}"
            )
