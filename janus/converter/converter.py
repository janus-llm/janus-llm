import functools
import json
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from openai import BadRequestError, RateLimitError
from pydantic import ValidationError

from janus.embedding.vectorize import ChromaDBVectorizer
from janus.language.block import BlockCollection, CodeBlock, TranslatedCodeBlock
from janus.language.combine import Combiner
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.language.splitter import (
    EmptyTreeError,
    FileSizeError,
    Splitter,
    TokenLimitError,
)
from janus.llm.model_callbacks import get_model_callback
from janus.llm.models_info import MODEL_PROMPT_ENGINES, JanusModel, load_model
from janus.parsers.parser import GenericParser, JanusParser, JanusParserException
from janus.refiners.refiner import JanusRefiner

# from janus.refiners.refiner import BasicRefiner, Refiner
from janus.retrievers.retriever import (
    ActiveUsingsRetriever,
    JanusRetriever,
    LanguageDocsRetriever,
)
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

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
            if not tracked_vars or self._changed_attrs.intersection(tracked_vars):
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
        model: str = "gpt-4o",
        model_arguments: dict[str, Any] = {},
        source_language: str = "fortran",
        max_prompts: int = 10,
        max_tokens: int | None = None,
        prompt_templates: list[str] | str = ["simple"],
        db_path: str | None = None,
        db_config: dict[str, Any] | None = None,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        splitter_type: str = "file",
        refiner_types: list[type[JanusRefiner] | str] = [JanusRefiner],
        retriever_type: str | None = None,
        combine_output: bool = True,
        use_janus_inputs: bool = False,
        target_language: str = "json",
        target_version: str | None = None,
        input_types: set[str] | str | None = None,
        input_labels: set[str] | str | None = None,
        output_type: str | None = None,
        output_label: str | None = None,
    ) -> None:
        """Initialize a Converter instance.

        Arguments:
            source_language: The source programming language.
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are `"code"`, `"text"`, `"eval"`, and `None` (default). If `None`,
                the `Converter` assumes you won't be parsing an output (i.e., adding to an
                embedding DB).
            max_prompts: The maximum number of prompts to try before giving up.
            max_tokens: The maximum number of tokens to use in the LLM. If `None`, the
                converter will use half the model's token limit.
            prompt_templates: The name of the prompt templates to use.
            db_path: The path to the database to use for vectorization.
            db_config: The configuration for the database.
            protected_node_types: A set of node types that aren't to be merged.
            prune_node_types: A set of node types which should be pruned.
            splitter_type: The type of splitter to use. Valid values are `"file"`,
                `"tag"`, `"chunk"`, `"ast-strict"`, and `"ast-flex"`.
            refiner_type: The type of refiner to use. Valid values:
                - "parser"
                - "reflection"
                - None
            retriever_type: The type of retriever to use. Valid values:
                - "active_usings"
                - "language_docs"
                - None
            combine_output: Whether to combine the output into a single file or not.
            use_janus_inputs: Whether to use janus inputs or not.
            target_language: The target programming language.
            target_version: The target programming language version.
            input_types: The types of input to accept.
            input_labels: The labels of input to accept.
            output_type: The type of output to produce.
            output_label: The label of output to produce.
        """
        self._changed_attrs: set = set()

        self.max_prompts: int = max_prompts
        self._max_tokens: int | None = max_tokens
        self.override_token_limit: bool = max_tokens is not None
        self._combine_output = combine_output

        self._model_name: str
        self._custom_model_arguments: dict[str, Any]

        self._source_language: str
        self._source_suffixes: list[str]

        self._target_language: str
        self._target_suffix: str
        self._target_version: str | None
        self.set_target_language(target_language, target_version)
        self._use_janus_inputs = use_janus_inputs

        self._protected_node_types: tuple[str, ...] = ()
        self._prune_node_types: tuple[str, ...] = ()
        self._max_tokens: int | None = max_tokens
        self._prompt_template_names: list[str]
        self._db_path: str | None
        self._db_config: dict[str, Any] | None

        self._llm: JanusModel
        self._prompt: ChatPromptTemplate

        self._parser: JanusParser = GenericParser()
        self._base_parser: JanusParser = GenericParser()
        self._combiner: Combiner = Combiner()

        self._splitter_type: str
        self._refiner_types: list[type[JanusRefiner] | str]
        self._retriever_type: str | None

        self._splitter: Splitter
        self._refiner: JanusRefiner
        self._retriever: JanusRetriever

        self.set_splitter(splitter_type=splitter_type)
        self.set_refiner_types(refiner_types=refiner_types)
        self.set_retriever(retriever_type=retriever_type)
        self.set_model(model_name=model, **model_arguments)
        self.set_prompts(prompt_templates=prompt_templates)
        self.set_source_language(source_language)
        self.set_protected_node_types(protected_node_types)
        self.set_prune_node_types(prune_node_types)
        self.set_db_path(db_path=db_path)
        self.set_db_config(db_config=db_config)

        self._input_types = input_types
        self._input_labels = input_labels
        self._output_type = output_type
        self._output_label = output_label

        self._load_parameters()

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
        self._load_model()
        self._load_translation_chain()
        self._load_retriever()
        self._load_refiner_chain()
        self._load_splitter()
        self._load_vectorizer()
        self._load_chain()
        self._changed_attrs.clear()

    def set_model(self, model_name: str, **custom_arguments: dict[str, Any]):
        """Validate and set the model name.

        The affected objects will not be updated until translate() is called.

        Arguments:
            model_name: The name of the model to use. Valid models are found in
                `janus.llm.models_info.MODEL_CONSTRUCTORS`.
            custom_arguments: Additional arguments to pass to the model constructor.
        """
        self._model_name = model_name
        self._custom_model_arguments = custom_arguments

    def set_prompts(self, prompt_templates: list[str] | str) -> None:
        """Validate and set the prompt template name.

        Arguments:
            prompt_templates: name of prompt template directories
                (see janus/prompts/templates) or paths to directories.
        """
        if isinstance(prompt_templates, str):
            self._prompt_template_names = [prompt_templates]
        else:
            self._prompt_template_names = prompt_templates

    def set_splitter(self, splitter_type: str) -> None:
        """Validate and set the prompt template name.

        Arguments:
            splitter_type: the type of splitter to use
        """
        if splitter_type not in CUSTOM_SPLITTERS:
            raise ValueError(f'Splitter type "{splitter_type}" does not exist.')

        self._splitter_type = splitter_type

    def set_refiner_types(self, refiner_types: list[type[JanusRefiner] | str]) -> None:
        """Validate and set the refiner type

        Arguments:
            refiner_type: the type of refiner to use
        """
        self._refiner_types = refiner_types

    def set_retriever(self, retriever_type: str | None) -> None:
        """Validate and set the retriever type

        Arguments:
            retriever_type: the type of retriever to use
        """
        self._retriever_type = retriever_type

    def set_source_language(self, source_language: str) -> None:
        """Validate and set the source language.

        Arguments:
            source_language: The source programming language.
        """
        source_language = source_language.lower()
        if source_language not in LANGUAGES:
            raise ValueError(
                f"Invalid source language: {source_language}. "
                "Valid source languages are found in `janus.utils.enums.LANGUAGES`."
            )

        self._source_suffixes = [
            f".{ext}" for ext in LANGUAGES[source_language]["suffixes"]
        ]

        self._source_language = source_language

    def set_protected_node_types(self, protected_node_types: tuple[str, ...]) -> None:
        """Set the protected (non-mergeable) node types. This will often be structures
        like functions, classes, or modules which you might want to keep separate

        The affected objects will not be updated until _load_parameters() is called.

        Arguments:
            protected_node_types: A set of node types that aren't to be merged
        """
        self._protected_node_types = tuple(set(protected_node_types or []))

    def set_prune_node_types(self, prune_node_types: tuple[str, ...]) -> None:
        """Set the node types to prune. This will often be structures
        like comments or whitespace which you might want to keep out of the LLM

        The affected objects will not be updated until _load_parameters() is called.

        Arguments:
            prune_node_types: A set of node types which should be pruned
        """
        self._prune_node_types = tuple(set(prune_node_types or []))

    def set_db_path(self, db_path: str | None) -> None:
        self._db_path = db_path

    def set_db_config(self, db_config: dict[str, Any] | None) -> None:
        self._db_config = db_config

    @run_if_changed(
        "_source_language",
        "_max_tokens",
        "_llm",
        "_protected_node_types",
        "_prune_node_types",
        "_custom_splitter",
    )
    def _load_splitter(self) -> None:
        """Load the splitter according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        kwargs: dict[str, Any] = dict(
            language=self._source_language,
            max_tokens=self._max_tokens,
            model=self._llm,
            protected_node_types=self._protected_node_types,
            prune_node_types=self._prune_node_types,
        )

        if self._splitter_type == "tag":
            kwargs["tag"] = "<ITMOD_ALC_SPLIT>"  # Hardcoded for now

        self._splitter = CUSTOM_SPLITTERS[self._splitter_type](**kwargs)

    @run_if_changed("_model_name", "_custom_model_arguments")
    def _load_model(self) -> None:
        """Load the model according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """

        # Get default arguments, set custom ones
        # model_arguments = deepcopy(MODEL_DEFAULT_ARGUMENTS[self._model_name])
        # model_arguments.update(self._custom_model_arguments)

        # Load the model
        self._llm = load_model(self._model_name)
        token_limit = self._llm.token_limit

        # Set the max_tokens to less than half the model's limit to allow for enough
        # tokens at output
        # Only modify max_tokens if it is not specified by user
        if not self.override_token_limit:
            self._max_tokens = int(token_limit * self._llm.input_token_proportion)

    @run_if_changed(
        "_prompt_template_names",
        "_source_language",
        "_model_name",
        "_target_language",
        "_target_version",
    )
    def _load_translation_chain(self) -> None:
        prompt_template_name = self._prompt_template_names[0]
        prompt_engine = MODEL_PROMPT_ENGINES[self._llm.short_model_id](
            source_language=self._source_language,
            prompt_template=prompt_template_name,
            target_language=self._target_language,
            target_version=self._target_version,
        )
        prompt = prompt_engine.prompt
        self._translation_chain = RunnableParallel(
            prompt_value=lambda x, prompt=prompt: prompt.invoke(x),
            original_inputs=RunnablePassthrough(),
        ) | RunnableParallel(
            completion=lambda x: self._llm.invoke(x["prompt_value"]),
            original_inputs=lambda x: x["original_inputs"],
            prompt_value=lambda x: x["prompt_value"],
        )
        for prompt_template_name in self._prompt_template_names[1:]:
            prompt_engine = MODEL_PROMPT_ENGINES[self._llm.short_model_id](
                source_language=self._source_language,
                prompt_template=prompt_template_name,
                target_language=self._target_language,
                target_version=self._target_version,
            )
            prompt = prompt_engine.prompt
            self._translation_chain = (
                self._translation_chain
                | RunnableParallel(
                    prompt_value=lambda x, prompt=prompt: prompt.invoke(
                        dict(completion=x["completion"], **x["original_inputs"])
                    ),
                    original_inputs=lambda x: x["original_inputs"],
                )
                | RunnableParallel(
                    completion=lambda x: self._llm.invoke(x["prompt_value"]),
                    original_inputs=lambda x: x["original_inputs"],
                    prompt_value=lambda x: x["prompt_value"],
                )
            )

    @run_if_changed("_db_path", "_db_config")
    def _load_vectorizer(self) -> None:
        if self._db_path is None or self._db_config is None:
            self._vectorizer = None
            return
        vectorizer_factory = ChromaDBVectorizer()
        self._vectorizer = vectorizer_factory.create_vectorizer(
            self._db_path, self._db_config
        )

    @run_if_changed("_retriever_type")
    def _load_retriever(self):
        if self._retriever_type == "active_usings":
            self._retriever = ActiveUsingsRetriever()
        elif self._retriever_type == "language_docs":
            self._retriever = LanguageDocsRetriever(self._llm, self._source_language)
        else:
            self._retriever = JanusRetriever()

    @run_if_changed("_refiner_types", "_model_name", "max_prompts", "_parser")
    def _load_refiner_chain(self) -> None:
        from janus.cli.constants import REFINERS

        if len(self._refiner_types) == 0:
            self._refiner_chain = RunnableLambda(
                lambda x: self._parser.parse(x["completion"])
            )
            return
        refiner_type = self._refiner_types[0]
        if isinstance(refiner_type, str):
            if refiner_type not in REFINERS:
                raise ValueError(f"Error: unable to find refiner type {refiner_type}")
            refiner_type = REFINERS[refiner_type]
        if len(self._refiner_types) == 1:
            self._refiner_chain = RunnableLambda(
                lambda x, refiner_type=refiner_type: refiner_type(
                    llm=self._llm,
                    parser=self._parser,
                    max_retries=self.max_prompts,
                ).parse_completion(**x)
            )
            return
        else:
            self._refiner_chain = RunnableParallel(
                completion=lambda x, refiner_type=refiner_type: refiner_type(
                    llm=self._llm,
                    parser=self._base_parser,
                    max_retries=self.max_prompts,
                ).parse_completion(**x),
                prompt_value=lambda x: x["prompt_value"],
            )
        for refiner_type in self._refiner_types[1:-1]:
            if isinstance(refiner_type, str):
                if refiner_type not in REFINERS:
                    raise ValueError(f"Error: unable to find refiner type {refiner_type}")
                refiner_type = REFINERS[refiner_type]
            # NOTE: Do NOT remove refiner_type=refiner_type from lambda.
            # Due to lambda capture, must be present or chain will not
            # be correctly constructed.
            self._refiner_chain = self._refiner_chain | RunnableParallel(
                completion=lambda x, refiner_type=refiner_type: refiner_type(
                    llm=self._llm,
                    parser=self._base_parser,
                    max_retries=self.max_prompts,
                ).parse_completion(**x),
                prompt_value=lambda x: x["prompt_value"],
            )
        self._refiner_chain = self._refiner_chain | RunnableLambda(
            lambda x: self._refiner_types[-1](
                llm=self._llm,
                parser=self._parser,
                max_retries=self.max_prompts,
            ).parse_completion(**x)
        )

    @run_if_changed(
        "_parser",
        "_retriever",
        "_prompt",
        "_llm",
        "_refiner_chain",
        "_target_language",
        "_target_version",
    )
    def _load_chain(self):
        self.chain = self.get_chain()

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
        )

    def get_chain(self) -> Runnable:
        """
        Gets a chain that can be executed by langchain
        """
        return self._input_runnable() | self._translation_chain | self._refiner_chain

    def translate(
        self,
        input_directory: str | Path,
        output_directory: str | Path | None = None,
        failure_directory: str | Path | None = None,
        overwrite: bool = False,
        collection_name: str | None = None,
    ) -> None:
        """Convert code in the input directory from the source language to the target
        language, and write the resulting files to the output directory.

        Arguments:
            input_directory: The directory containing the code to translate.
            output_directory: The directory to write the translated code to.
            overwrite: Whether to overwrite existing files (vs skip them)
            collection_name: Collection to add to
        """
        # Convert paths to pathlib Paths if needed
        if isinstance(input_directory, str):
            input_directory = Path(input_directory)
        if isinstance(output_directory, str):
            output_directory = Path(output_directory)
        if isinstance(failure_directory, str):
            failure_directory = Path(failure_directory)

        # Make sure the output directory exists
        if output_directory is not None and not output_directory.exists():
            output_directory.mkdir(parents=True)
        if failure_directory is not None and not failure_directory.exists():
            failure_directory.mkdir(parents=True)

        input_paths = []
        if self._use_janus_inputs:
            source_language = "janus"
            source_suffixes = [".json"]
        else:
            source_language = self._source_language
            source_suffixes = self._source_suffixes
        for ext in source_suffixes:
            input_paths.extend(input_directory.rglob(f"**/*{ext}"))

        log.info(f"Input directory: {input_directory.absolute()}")
        log.info(f"{source_language} {source_suffixes} files: " f"{len(input_paths)}")
        log.info(
            "Other files (skipped): "
            f"{len(list(input_directory.iterdir())) - len(input_paths)}\n"
        )
        if output_directory is not None:
            output_paths = [
                output_directory / p.relative_to(input_directory).with_suffix(".json")
                for p in input_paths
            ]
        else:
            output_paths = [None for _ in input_paths]

        if failure_directory is not None:
            failure_paths = [
                failure_directory / p.relative_to(input_directory).with_suffix(".json")
                for p in input_paths
            ]
        else:
            failure_paths = [None for _ in input_paths]
        in_out_pairs = list(zip(input_paths, output_paths, failure_paths))
        if not overwrite:
            n_files = len(in_out_pairs)
            in_out_pairs = [
                (inp, outp, failp)
                for inp, outp, failp in in_out_pairs
                if outp is None or not outp.exists()
            ]
            log.info(
                f"Skipping {n_files - len(in_out_pairs)} existing "
                f"{self._source_suffixes} files"
            )
        log.info(f"Translating {len(in_out_pairs)} {self._source_suffixes} files")

        # Loop through each input file, convert and save it
        total_cost = 0.0
        for in_path, out_path, fail_path in in_out_pairs:
            # Translate the file, skip it if there's a rate limit error
            log.info(f"Processing {in_path.relative_to(input_directory)}")
            if self._use_janus_inputs:
                out_block = self.translate_janus_file(in_path, fail_path)
            else:
                out_block = self.translate_file(in_path, fail_path)

            def _get_total_cost(block):
                if isinstance(block, list):
                    return sum(_get_total_cost(b) for b in block)
                return block.total_cost

            total_cost += _get_total_cost(out_block)
            log.info(f"Current Running Cost: {total_cost}")

            # For files where translation failed, write to failure path instead

            def _has_empty(block):
                if isinstance(block, BlockCollection):
                    return len(block.blocks) == 0 or any(
                        _has_empty(b) for b in block.blocks
                    )
                return not block.translated

            if _has_empty(out_block):
                if fail_path is not None:
                    self._save_to_file(out_block, fail_path)
                continue

            if collection_name is not None:
                self._vectorizer.add_nodes_recursively(
                    out_block,
                    collection_name,
                    in_path.name,
                )

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            for b in out_block.blocks:
                self._combiner.combine(b)
            if out_path is not None and (overwrite or not out_path.exists()):
                self._save_to_file(out_block, out_path)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def _filter_blocks(self, code_block):
        if isinstance(code_block, BlockCollection):
            input_blocks = list(code_block.blocks)
        else:
            input_blocks = [code_block]
        if self._input_types is not None:
            if isinstance(self._input_types, str):
                self._input_types = set([self._input_types])
            input_blocks = [
                b
                for b in input_blocks
                if isinstance(b, BlockCollection) or b.block_type in self._input_types
            ]
        if self._input_labels is not None:
            if isinstance(self._input_labels, str):
                self._input_labels = set([self._input_labels])
            input_blocks = [
                b
                for b in input_blocks
                if isinstance(b, BlockCollection) or b.block_label in self._input_labels
            ]
        return input_blocks

    def translate_blocks(
        self,
        code_block: CodeBlock | BlockCollection,
        failure_path: Path | None = None,
    ) -> BlockCollection | TranslatedCodeBlock:
        input_blocks = self._filter_blocks(code_block)
        output_blocks = []
        for b in input_blocks:
            output_blocks.append(self.translate_block(b, failure_path))
        return BlockCollection(output_blocks, code_block.previous_generations)

    def translate_block(
        self,
        input_block: CodeBlock,
        failure_path: Path | None = None,
    ) -> TranslatedCodeBlock:
        self._load_parameters()
        output_block = self._iterative_translate(input_block, failure_path)
        if output_block.translated:
            completeness = output_block.translation_completeness
            log.info(
                f"[{output_block.name}] Translation complete\n"
                f"  {completeness:.2%} of input successfully translated\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Output CodeBlock Structure:\n{input_block.tree_str()}\n"
            )

        else:
            log.error(
                f"[{output_block.name}] Translation failed\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
            )
        return output_block

    def translate_file(
        self,
        file: Path,
        failure_path: Path | None = None,
    ) -> TranslatedCodeBlock:
        """Translate a single file.

        Arguments:
            file: Input path to file
            failure_path: path to directory to store failure summaries`

        Returns:
            A `TranslatedCodeBlock` object. This block does not have a path set, and its
            code is not guaranteed to be consolidated. To amend this, run
            `Combiner.combine_children` on the block.
        """
        input_block = self._split_file(file)
        return self.translate_blocks(input_block, failure_path)

    def translate_janus_file(self, file: Path, failure_path: Path | None = None):
        filename = file.name
        with open(file, "r") as f:
            file_obj = json.load(f)
        return self.translate_janus_obj(file_obj, filename, failure_path)

    def translate_janus_obj(self, obj: Any, name: str, failure_path: Path | None = None):
        block = self._janus_object_to_codeblock(obj, name)
        return self.translate_blocks(block, failure_path)

    def translate_text(self, text: str, name: str, failure_path: Path | None = None):
        """
        Translates given text
        Arguments:
            text: text to translate
            name: the name of the text (filename if from a file)
            failure_path: path to write failure file if translation is not successful
        """
        input_block = self._split_text(text, name)
        return self.translate_blocks(input_block, failure_path)

    def _iterative_translate(
        self, root: CodeBlock, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        """Translate the passed CodeBlock representing a full file.

        Arguments:
            root: A root block representing the top-level block of a file
            failure_path: path to store data files for failed translations

        Returns:
            A `TranslatedCodeBlock`
        """
        translated_root = TranslatedCodeBlock(
            root,
            self._target_language,
            self,
            block_type=self._output_type,
            block_label=self._output_label,
        )
        last_prog, prog_delta = 0, 0.1
        stack = [translated_root]
        try:
            while stack:
                translated_block = stack.pop()

                self._add_translation(translated_block)

                # If translating this block was unsuccessful, don't bother with its
                #  children (they wouldn't show up in the final text anyway)
                if not translated_block.translated:
                    continue

                stack.extend(translated_block.children)

                progress = translated_root.translation_completeness
                if progress - last_prog > prog_delta:
                    last_prog = int(progress / prog_delta) * prog_delta
                    log.info(f"[{root.name}] progress: {progress:.2%}")
        except RateLimitError:
            pass
        except OutputParserException as e:
            log.error(f"Skipping file, failed to parse output: {e}")
        except BadRequestError as e:
            if str(e).startswith("Detected an error in the prompt"):
                log.warning("Malformed input, skipping")
            raise e
        except ValidationError as e:
            # Only allow ValidationError to pass if token limit is manually set
            if self.override_token_limit:
                log.warning(
                    "Current file and manually set token "
                    "limit is too large for this model, skipping"
                )
            raise e
        except TokenLimitError:
            log.warning("Ran into irreducible node too large for context, skipping")
        except EmptyTreeError:
            log.warning("Input file has no nodes of interest, skipping")
        except FileSizeError:
            log.warning("Current tile is too large for basic splitter, skipping")
        except ValueError as e:
            if str(e).startswith(
                "Error raised by bedrock service"
            ) and "maximum context length" in str(e):
                log.warning(
                    "Input is too large for this model's context length, skipping"
                )
            raise e
        finally:
            out_obj = self._get_output_obj(
                translated_root, self._combine_output, include_previous_outputs=True
            )
            log.debug(f"Resulting Block:" f"{json.dumps(out_obj)}")
            if not translated_root.translated:
                if failure_path is not None:
                    self._save_to_file(translated_root, failure_path)

        return translated_root

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        """Given an "empty" `TranslatedCodeBlock`, translate the code represented in
        `block.original`, setting the relevant fields in the translated block. The
        `TranslatedCodeBlock` is updated in-pace, nothing is returned. Note that this
        translates *only* the code for this block, not its children.

        Arguments:
            block: An empty `TranslatedCodeBlock`
        """
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self._llm is None:
            message = (
                "Model not configured correctly, cannot translate. Try setting "
                "the model"
            )
            log.error(message)
            raise ValueError(message)

        log.debug(f"[{block.name}] Translating...")
        log.debug(f"[{block.name}] Input text:\n{block.original.text}")

        # Track the cost of translating this block
        #  TODO: If non-OpenAI models with prices are added, this will need
        #   to be updated.
        with get_model_callback() as cb:
            try:
                t0 = time.time()
                block.text = self._run_chain(block)
            except JanusParserException as e:
                block.text = e.unparsed_output
                block.tokens = self._llm.get_num_tokens(block.text)
                raise e
            finally:
                block.processing_time = time.time() - t0
                block.cost = cb.total_cost
                block.request_input_tokens = cb.prompt_tokens
                block.request_output_tokens = cb.completion_tokens
                block.num_requests = cb.successful_requests

        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(f"[{block.name}] Output code:\n{block.text}")

    def _split_text(self, text: str, name: str) -> CodeBlock:
        log.info(f"[{name}] Splitting text")
        root = self._splitter.split_string(text, name)
        log.info(
            f"[{name}] Text split into {root.n_descendents:,} blocks,"
            f"tree of height {root.height}"
        )
        log.info(f"[{name}] Input CodeBlock Structure:\n{root.tree_str()}")
        return root

    def _split_file(self, file: Path) -> CodeBlock:
        filename = file.name
        log.info(f"[{filename}] Splitting file")
        root = self._splitter.split(file)
        log.info(
            f"[{filename}] File split into {root.n_descendents:,} blocks, "
            f"tree of height {root.height}"
        )
        log.info(f"[{filename}] Input CodeBlock Structure:\n{root.tree_str()}")
        return root

    def _run_chain(self, block: TranslatedCodeBlock) -> str:
        return self.chain.invoke(block.original)

    def _combine_metadata(self, metadatas: list[dict]):
        return dict(
            cost=sum(m["cost"] for m in metadatas),
            processing_time=sum(m["processing_time"] for m in metadatas),
            num_requests=sum(m["num_requests"] for m in metadatas),
            input_tokens=sum(m["input_tokens"] for m in metadatas),
            output_tokens=sum(m["output_tokens"] for m in metadatas),
            converter_name=self.__class__.__name__,
            type=[m["type"] for m in metadatas],
            label=[m["label"] for m in metadatas],
        )

    def _combine_inputs(self, inputs: list[str]):
        return json.dumps(inputs)

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | BlockCollection | dict,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        block_type = None
        block_label = None
        if isinstance(block, dict):
            # output object has already been generated
            new_block = deepcopy(block)
            if "intermediate_outputs" in new_block:
                del new_block["intermediate_outputs"]
            return new_block
        if isinstance(block, BlockCollection):
            if len(block.blocks) == 1:
                outputs = self._get_output_obj(block.blocks[0], combine_children, False)[
                    "outputs"
                ]
                block_type = block.blocks[0].block_type
                block_label = block.blocks[0].block_label
            else:
                outputs = [
                    self._get_output_obj(b, combine_children, False) for b in block.blocks
                ]
        elif (
            not isinstance(block, BlockCollection)
            and not combine_children
            and len(block.children) > 0
        ):
            outputs = self._get_output_obj_children(block, False)
        else:
            block_type = block.block_type
            block_label = block.block_label
            if not block.translation_completed:
                # translation wasn't completed, so combined parsing will likely fail
                outputs = [block.complete_text]
            else:
                output_str = self._parser.parse_combined_output(block.complete_text)
                outputs = [output_str]

        def _get_input(block):
            if isinstance(block, BlockCollection):
                return self._combine_inputs([_get_input(b) for b in block.blocks])
            return block.original.text or ""

        out = dict(
            input=_get_input(block),
            metadata=dict(
                cost=block.total_cost,
                processing_time=block.total_processing_time,
                num_requests=block.total_num_requests,
                input_tokens=block.total_request_input_tokens,
                output_tokens=block.total_request_output_tokens,
                converter_name=self.__class__.__name__,
                type=block_type,
                label=block_label,
            ),
            outputs=outputs,
        )
        if (
            include_previous_outputs
            and isinstance(block, BlockCollection)
            and len(block.previous_generations) > 0
        ):
            intermediate_outputs = []
            for p in block.previous_generations:
                if isinstance(p, dict):
                    # preserve intermediate outputs from previous runs
                    intermediate_outputs.append(
                        self._get_output_obj(p, combine_children, False)
                    )
            if len(intermediate_outputs) > 0:
                out["intermediate_outputs"] = intermediate_outputs
        return out

    def _get_output_obj_children(
        self, block: TranslatedCodeBlock, include_previous_outputs: bool = True
    ):
        if len(block.children) > 0:
            res = []
            for c in block.children:
                res += self._get_output_obj_children(c, include_previous_outputs)
            return res
        else:
            return [
                self._get_output_obj(
                    block,
                    combine_children=True,
                    include_previous_outputs=include_previous_outputs,
                )
            ]

    def _save_to_file(self, block: TranslatedCodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `TranslatedCodeBlock` to save to a file.
        """
        obj = self._get_output_obj(
            block, combine_children=self._combine_output, include_previous_outputs=True
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

    def _janus_object_to_codeblock(self, janus_obj: dict, name: str):
        results = []
        for o in janus_obj["outputs"]:
            metadata = janus_obj["metadata"]
            if isinstance(o, str):
                block_label = metadata["label"]
                if isinstance(block_label, list):
                    block_label = block_label[0]
                block_type = metadata["type"]
                if isinstance(block_type, list):
                    block_type = block_type[0]
                code_block = self._split_text(o, name)
                code_block.previous_generations = janus_obj.get(
                    "intermediate_outputs", []
                ) + [janus_obj]
                code_block.block_type = block_type
                code_block.block_label = block_label
                results.append(code_block)
            else:
                results += self._janus_object_to_codeblock(o, name).blocks
        previous_generations = janus_obj.get("intermediate_outputs", [])
        if janus_obj["metadata"]["converter_name"] != "ConverterChain":
            previous_generations += [janus_obj]
        return BlockCollection(results, previous_generations)

    def __or__(self, other: "Converter"):
        from janus.converter.chain import ConverterChain

        return ConverterChain(self, other)

    @property
    def source_language(self):
        return self._source_language

    @property
    def target_language(self):
        return self._target_language

    @property
    def target_version(self):
        return self._target_version

    def set_target_language(
        self, target_language: str, target_version: str | None
    ) -> None:
        """Validate and set the target language.

        The affected objects will not be updated until translate() is called.

        Arguments:
            target_language: The target programming language.
            target_version: The target version of the target programming language.
        """
        target_language = target_language.lower()
        if target_language not in LANGUAGES:
            raise ValueError(
                f"Invalid target language: {target_language}. "
                "Valid target languages are found in `janus.utils.enums.LANGUAGES`."
            )
        self._target_language = target_language
        self._target_version = target_version
        # Taking the first suffix as the default for output files
        self._target_suffix = f".{LANGUAGES[target_language]['suffixes'][0]}"

    @classmethod
    def eval_obj(cls, target, metric_func, *args, **kwargs):
        if "reference" in kwargs:
            return cls.eval_obj_reference(target, metric_func, *args, **kwargs)
        else:
            return cls.eval_obj_noreference(target, metric_func, *args, **kwargs)

    @classmethod
    def eval_obj_noreference(cls, target, metric_func, *args, **kwargs):
        results = []
        for o in target["outputs"]:
            if isinstance(o, dict):
                results += cls.eval_obj_noreference(o, metric_func, *args, **kwargs)
            else:
                results.append(metric_func(o, *args, **kwargs))
        return results

    @classmethod
    def eval_obj_reference(cls, target, metric_func, reference, *args, **kwargs):
        results = []
        for o, r in zip(target["outputs"], reference["outputs"]):
            if isinstance(o, dict):
                if not isinstance(r, dict):
                    raise ValueError("Error: format of reference doesn't match target")
                results += cls.eval_obj_reference(o, metric_func, r, *args, **kwargs)
            else:
                if isinstance(r, dict):
                    raise ValueError("Error: format of reference doesn't match target")
                results.append(metric_func(o, r, *args, **kwargs))
        return results
