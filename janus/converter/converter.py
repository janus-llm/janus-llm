import functools
import json
import time
from pathlib import Path
from typing import Any

from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from openai import BadRequestError, RateLimitError
from pydantic import ValidationError

from janus.embedding.vectorize import ChromaDBVectorizer
from janus.language.block import CodeBlock, TranslatedCodeBlock
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
from janus.parsers.parser import GenericParser, JanusParser
from janus.refiners.refiner import (
    FixParserExceptions,
    HallucinationRefiner,
    JanusRefiner,
    ReflectionRefiner,
)

# from janus.refiners.refiner import BasicRefiner, Refiner
from janus.retrievers.retriever import ActiveUsingsRetriever, JanusRetriever
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
        prompt_template: str = "simple",
        db_path: str | None = None,
        db_config: dict[str, Any] | None = None,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        splitter_type: str = "file",
        refiner_type: str | None = None,
        retriever_type: str | None = None,
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
            prompt_template: The name of the prompt template to use.
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
                - None
        """
        self._changed_attrs: set = set()

        self.max_prompts: int = max_prompts
        self._max_tokens: int | None = max_tokens
        self.override_token_limit: bool = max_tokens is not None

        self._model_name: str
        self._custom_model_arguments: dict[str, Any]

        self._source_language: str
        self._source_suffix: str

        self._target_language = "json"
        self._target_suffix = ".json"

        self._protected_node_types: tuple[str, ...] = ()
        self._prune_node_types: tuple[str, ...] = ()
        self._max_tokens: int | None = max_tokens
        self._prompt_template_name: str
        self._db_path: str | None
        self._db_config: dict[str, Any] | None

        self._llm: JanusModel
        self._prompt: ChatPromptTemplate

        self._parser: JanusParser = GenericParser()
        self._combiner: Combiner = Combiner()

        self._splitter_type: str
        self._refiner_type: str | None
        self._retriever_type: str | None

        self._splitter: Splitter
        self._refiner: JanusRefiner
        self._retriever: JanusRetriever

        self.set_splitter(splitter_type=splitter_type)
        self.set_refiner(refiner_type=refiner_type)
        self.set_retriever(retriever_type=retriever_type)
        self.set_model(model_name=model, **model_arguments)
        self.set_prompt(prompt_template=prompt_template)
        self.set_source_language(source_language)
        self.set_protected_node_types(protected_node_types)
        self.set_prune_node_types(prune_node_types)
        self.set_db_path(db_path=db_path)
        self.set_db_config(db_config=db_config)

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
        self._load_prompt()
        self._load_retriever()
        self._load_refiner()
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

    def set_prompt(self, prompt_template: str) -> None:
        """Validate and set the prompt template name.

        Arguments:
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        self._prompt_template_name = prompt_template

    def set_splitter(self, splitter_type: str) -> None:
        """Validate and set the prompt template name.

        Arguments:
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        if splitter_type not in CUSTOM_SPLITTERS:
            raise ValueError(f'Splitter type "{splitter_type}" does not exist.')

        self._splitter_type = splitter_type

    def set_refiner(self, refiner_type: str | None) -> None:
        """Validate and set the refiner type

        Arguments:
            refiner_type: the type of refiner to use
        """
        self._refiner_type = refiner_type

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

        ext = LANGUAGES[source_language]["suffix"]
        self._source_suffix = f".{ext}"
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
            self._max_tokens = int(token_limit // 2.5)

    @run_if_changed(
        "_prompt_template_name",
        "_source_language",
        "_model_name",
        "_parser",
    )
    def _load_prompt(self) -> None:
        """Load the prompt according to this instance's attributes.

        If the relevant fields have not been changed since the last time this
        method was called, nothing happens.
        """
        prompt_engine = MODEL_PROMPT_ENGINES[self._llm.short_model_id](
            source_language=self._source_language,
            prompt_template=self._prompt_template_name,
        )
        self._prompt = prompt_engine.prompt
        self._prompt = self._prompt.partial(
            format_instructions=self._parser.get_format_instructions()
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
        else:
            self._retriever = JanusRetriever()

    @run_if_changed("_refiner_type", "_model_name", "max_prompts", "_parser", "_llm")
    def _load_refiner(self) -> None:
        """Load the refiner according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        if self._refiner_type == "parser":
            self._refiner = FixParserExceptions(
                llm=self._llm,
                parser=self._parser,
                max_retries=self.max_prompts,
            )
        elif self._refiner_type == "reflection":
            self._refiner = ReflectionRefiner(
                llm=self._llm,
                parser=self._parser,
                max_retries=self.max_prompts,
            )
        elif self._refiner_type == "hallucination":
            self._refiner = HallucinationRefiner(
                llm=self._llm,
                parser=self._parser,
                max_retries=self.max_prompts,
            )
        else:
            self._refiner = JanusRefiner(parser=self._parser)

    @run_if_changed("_parser", "_retriever", "_prompt", "_llm", "_refiner")
    def _load_chain(self):
        self.chain = (
            self._input_runnable()
            | self._prompt
            | RunnableParallel(
                completion=self._llm,
                prompt_value=RunnablePassthrough(),
            )
            | self._refiner.parse_runnable
        )

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
        )

    def translate(
        self,
        input_directory: str | Path,
        output_directory: str | Path | None = None,
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

        # Make sure the output directory exists
        if output_directory is not None and not output_directory.exists():
            output_directory.mkdir(parents=True)

        input_paths = [p for p in input_directory.rglob(f"**/*{self._source_suffix}")]

        log.info(f"Input directory: {input_directory.absolute()}")
        log.info(
            f"{self._source_language} '*{self._source_suffix}' files: "
            f"{len(input_paths)}"
        )
        log.info(
            "Other files (skipped): "
            f"{len(list(input_directory.iterdir())) - len(input_paths)}\n"
        )
        if output_directory is not None:
            output_paths = [
                output_directory
                / p.relative_to(input_directory).with_suffix(self._target_suffix)
                for p in input_paths
            ]
            in_out_pairs = list(zip(input_paths, output_paths))
            if not overwrite:
                n_files = len(in_out_pairs)
                in_out_pairs = [
                    (inp, outp) for inp, outp in in_out_pairs if not outp.exists()
                ]
                log.info(
                    f"Skipping {n_files - len(in_out_pairs)} existing "
                    f"'*{self._source_suffix}' files"
                )
        else:
            in_out_pairs = [(f, None) for f in input_paths]
        log.info(f"Translating {len(in_out_pairs)} '*{self._source_suffix}' files")

        # Loop through each input file, convert and save it
        total_cost = 0.0
        for in_path, out_path in in_out_pairs:
            # Translate the file, skip it if there's a rate limit error
            try:
                out_block = self.translate_file(in_path)
                total_cost += out_block.total_cost
            except RateLimitError:
                continue
            except OutputParserException as e:
                log.error(f"Skipping {in_path.name}, failed to parse output: {e}.")
                continue
            except BadRequestError as e:
                if str(e).startswith("Detected an error in the prompt"):
                    log.warning("Malformed input, skipping")
                    continue
                raise e
            except ValidationError as e:
                # Only allow ValidationError to pass if token limit is manually set
                if self.override_token_limit:
                    log.warning(
                        "Current file and manually set token "
                        "limit is too large for this model, skipping"
                    )
                    continue
                raise e
            except TokenLimitError:
                log.warning("Ran into irreducible node too large for context, skipping")
                continue
            except EmptyTreeError:
                log.warning(
                    f'Input file "{in_path.name}" has no nodes of interest, skipping'
                )
                continue
            except FileSizeError:
                log.warning("Current tile is too large for basic splitter, skipping")
                continue
            except ValueError as e:
                if str(e).startswith(
                    "Error raised by bedrock service"
                ) and "maximum context length" in str(e):
                    log.warning(
                        "Input is too large for this model's context length, skipping"
                    )
                    continue
                raise e

            # Don't attempt to write files for which translation failed
            if not out_block.translated:
                continue

            if collection_name is not None:
                self._vectorizer.add_nodes_recursively(
                    out_block,
                    collection_name,
                    in_path.name,
                )

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            self._combiner.combine(out_block)
            if out_path is not None and (overwrite or not out_path.exists()):
                self._save_to_file(out_block, out_path)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def translate_file(self, file: Path) -> TranslatedCodeBlock:
        """Translate a single file.

        Arguments:
            file: Input path to file

        Returns:
            A `TranslatedCodeBlock` object. This block does not have a path set, and its
            code is not guaranteed to be consolidated. To amend this, run
            `Combiner.combine_children` on the block.
        """
        self._load_parameters()
        filename = file.name

        input_block = self._split_file(file)
        t0 = time.time()
        output_block = self._iterative_translate(input_block)
        output_block.processing_time = time.time() - t0
        if output_block.translated:
            completeness = output_block.translation_completeness
            log.info(
                f"[{filename}] Translation complete\n"
                f"  {completeness:.2%} of input successfully translated\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
                f"  Output CodeBlock Structure:\n{input_block.tree_str()}\n"
            )

        else:
            log.error(
                f"[{filename}] Translation failed\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
            )
        return output_block

    def _iterative_translate(self, root: CodeBlock) -> TranslatedCodeBlock:
        """Translate the passed CodeBlock representing a full file.

        Arguments:
            root: A root block representing the top-level block of a file

        Returns:
            A `TranslatedCodeBlock`
        """
        translated_root = TranslatedCodeBlock(root, self._target_language)
        last_prog, prog_delta = 0, 0.1
        stack = [translated_root]
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
            t0 = time.time()
            block.text = self._run_chain(block)
            block.processing_time = time.time() - t0
            block.cost = cb.total_cost
            block.retries = max(0, cb.successful_requests - 1)

        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(f"[{block.name}] Output code:\n{block.text}")

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

    def _get_output_obj(
        self, block: TranslatedCodeBlock
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        output_str = self._parser.parse_combined_output(block.complete_text)

        output_obj: str | dict[str, str]
        try:
            output_obj = json.loads(output_str)
        except json.JSONDecodeError:
            output_obj = output_str

        return dict(
            input=block.original.text or "",
            metadata=dict(
                retries=block.total_retries,
                cost=block.total_cost,
                processing_time=block.processing_time,
            ),
            output=output_obj,
        )

    def _save_to_file(self, block: TranslatedCodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `TranslatedCodeBlock` to save to a file.
        """
        obj = self._get_output_obj(block)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
