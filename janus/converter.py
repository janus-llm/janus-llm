import functools
from typing import Any

from langchain.schema.language_model import BaseLanguageModel

from .language.binary import BinarySplitter
from .language.mumps import MumpsSplitter
from .language.splitter import Splitter
from .language.treesitter import TreeSitterSplitter
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
        max_tokens: None | int = None,
        protected_node_types: set[str] | list[str] | tuple[str] = (),
        prune_node_types: set[str] | list[str] | tuple[str] = (),
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

        self._source_language: None | str
        self._source_glob: None | str
        self._protected_node_types: tuple[str] = ()
        self._prune_node_types: tuple[str] = ()
        self._splitter: None | Splitter
        self._llm: None | BaseLanguageModel = None
        self._max_tokens: None | int = max_tokens

        self.set_source_language(source_language)
        self.set_protected_node_types(protected_node_types)
        self.set_prune_node_types(prune_node_types)

        # Child class must call this. Should we enforce somehow?
        # self._load_parameters()

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
        self._changed_attrs.clear()

    def set_source_language(self, source_language: str) -> None:
        """Validate and set the source language.

        The affected objects will not be updated until _load_parameters() is called.

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

    def set_protected_node_types(
        self, protected_node_types: set[str] | list[str] | tuple[str]
    ) -> None:
        """Set the protected (non-mergeable) node types. This will often be structures
        like functions, classes, or modules which you might want to keep separate

        The affected objects will not be updated until _load_parameters() is called.

        Arguments:
            protected_node_types: A set of node types that aren't to be merged
        """
        self._protected_node_types = tuple(set(protected_node_types or []))

    def set_prune_node_types(
        self, prune_node_types: set[str] | list[str] | tuple[str]
    ) -> None:
        """Set the node types to prune. This will often be structures
        like comments or whitespace which you might want to keep out of the LLM

        The affected objects will not be updated until _load_parameters() is called.

        Arguments:
            prune_node_types: A set of node types which should be pruned
        """
        self._prune_node_types = tuple(set(prune_node_types or []))

    @run_if_changed(
        "_source_language",
        "_max_tokens",
        "_llm",
        "_protected_node_types",
        "_prune_node_types",
    )
    def _load_splitter(self) -> None:
        """Load the splitter according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        kwargs = dict(
            max_tokens=self._max_tokens,
            model=self._llm,
            protected_node_types=self._protected_node_types,
            prune_node_types=self._prune_node_types,
        )
        if self._source_language in CUSTOM_SPLITTERS:
            if self._source_language == "mumps":
                self._splitter = MumpsSplitter(**kwargs)
            elif self._source_language == "binary":
                self._splitter = BinarySplitter(**kwargs)
        else:
            self._splitter = TreeSitterSplitter(language=self._source_language, **kwargs)
