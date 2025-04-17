import json
import time
from copy import deepcopy
from operator import itemgetter
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

from janus.cli.constants import REFINERS
from janus.converter.chain import ConverterChain
from janus.embedding.vectorize import ChromaDBVectorizer, Vectorizer
from janus.language.block import (
    BlockCollection,
    CodeBlock,
    JanusOutputObject,
    TranslatedBlockCollection,
    TranslatedCodeBlock,
)
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
            protected_node_types: A set of non-mergeable node types. These will
                often be structures like functions, classes, or modules which
                you might want to keep separate.
            prune_node_types: A set of node types to prune. These will often be
                structures like comments or whitespace which you might want to
                keep out of the LLM.
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
        # Set source language and suffix
        self._source_language: str
        self._source_suffixes: list[str]
        self._set_source_language(source_language)

        # Set target language and suffix
        self._target_language: str
        self._target_suffix: str
        self._target_version: str | None
        self._set_target_language(target_language, target_version)

        # Set splitter
        self._splitter_type: str
        self._set_splitter(splitter_type=splitter_type)

        # Set refiner types
        self._refiner_types: list[type[JanusRefiner]]
        self._set_refiner_types(refiner_types=refiner_types)

        # Set input token limit
        self._max_tokens: int | None
        self._override_token_limit: bool
        self._set_input_token_limit(max_tokens=max_tokens)

        # Set simple members
        self._model_name: str = model
        self._max_prompts: int = max_prompts
        self._combine_output = combine_output
        self._db_path: str | None = db_path
        self._db_config: dict[str, Any] | None = db_config
        self._retriever_type: str | None = retriever_type
        self._use_janus_inputs: bool = use_janus_inputs
        self._output_type: str | None = output_type
        self._output_label: str | None = output_label

        if isinstance(input_types, str):
            input_types = set([input_types])
        if isinstance(input_labels, str):
            input_labels = set([input_labels])
        self._input_types: set[str] | None = input_types
        self._input_labels: set[str] | None = input_labels

        # Set the list of prompt templates. If a single string was passed, make it
        #  a single-element list for compatibility
        self._prompt_template_names: list[str] = (
            prompt_templates if isinstance(prompt_templates, list) else [prompt_templates]
        )

        # Make sure protected and pruned node types are unique
        self._protected_node_types: tuple[str, ...] = tuple(set(protected_node_types))
        self._prune_node_types: tuple[str, ...] = tuple(set(prune_node_types))

        # Default parsers and combiners do nothing
        self._parser: JanusParser = GenericParser()
        self._base_parser: JanusParser = GenericParser()
        self._combiner: Combiner = Combiner()

        # Declare types of objects to be loaded
        self._llm: JanusModel
        self._splitter: Splitter
        self._retriever: JanusRetriever
        self._vectorizer: Vectorizer | None
        self._prompts: list[ChatPromptTemplate]
        self._chain: Runnable

        self._initialized = False

    def _load_parameters(self) -> None:
        if self._initialized:
            return

        self._load_model()
        self._load_splitter()
        self._load_retriever()
        self._load_vectorizer()
        self._load_prompts()
        self._load_chain()

        self._initialized = True

    def _set_splitter(self, splitter_type: str) -> None:
        """Validate and set the splitter type

        Arguments:
            retriever_type: the type of splitter to use, must be one of CUSTOM_SPLITTERS
        """
        if splitter_type not in CUSTOM_SPLITTERS:
            raise ValueError(f'Splitter type "{splitter_type}" does not exist.')

        self._splitter_type = splitter_type

    def _set_refiner_types(self, refiner_types: list[type[JanusRefiner] | str]) -> None:
        self._refiner_types = []
        for refiner_type in refiner_types:
            if isinstance(refiner_type, str):
                if refiner_type not in REFINERS:
                    raise ValueError(f"Error: unable to find refiner type {refiner_type}")
                self._refiner_types.append(REFINERS[refiner_type])
            else:
                self._refiner_types.append(refiner_type)

    def _set_source_language(self, source_language: str) -> None:
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

    def _set_target_language(
        self, target_language: str, target_version: str | None
    ) -> None:
        """Validate and set the target language.

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

    def _set_input_token_limit(self, max_tokens: int | None) -> None:
        """Validate and set the input token limit.

        Arguments:
            max_tokens: The maximum input length in tokens.
        """
        self._max_tokens = max_tokens
        self._override_token_limit = max_tokens is not None

    def _load_model(self):
        """Impacts:
        _llm
        _max_tokens

        Depends on:
        _model_name
        _max_tokens
        """
        # Load the model
        self._llm = load_model(self._model_name)

        # Set the max_tokens to less than half the model's limit to allow for enough
        # tokens at output
        # Only modify max_tokens if it is not specified by user
        if not self._override_token_limit:
            self._max_tokens = int(
                self._llm.token_limit * self._llm.input_token_proportion
            )

    def _load_splitter(self) -> None:
        """Impacts:
        _splitter

        Depends on:
        _splitter_type
        _source_language
        _max_tokens
        _llm
        _protected_node_types
        _prune_node_types
        """
        kwargs = dict()
        if self._splitter_type == "tag":
            kwargs["tag"] = "<JANUS_PARTITION>"  # Hardcoded for now

        self._splitter = CUSTOM_SPLITTERS[self._splitter_type](
            language=self._source_language,
            max_tokens=self._max_tokens,
            model=self._llm,
            protected_node_types=self._protected_node_types,
            prune_node_types=self._prune_node_types,
            **kwargs,
        )

    def _load_retriever(self) -> None:
        """Impacts:
        _retriever

        Depends on:
        _retriever_type
        _llm
        _source_language
        """
        if self._retriever_type == "active_usings":
            self._retriever = ActiveUsingsRetriever()
        elif self._retriever_type == "language_docs":
            self._retriever = LanguageDocsRetriever(self._llm, self._source_language)
        else:
            self._retriever = JanusRetriever()

    def _load_vectorizer(self) -> None:
        """Impacts:
        _vectorizer

        Depends on:
        _db_path
        _db_config
        """
        if self._db_path is None or self._db_config is None:
            self._vectorizer = None
            return
        vectorizer_factory = ChromaDBVectorizer()
        self._vectorizer = vectorizer_factory.create_vectorizer(
            self._db_path,
            self._db_config,
        )

    def _load_prompts(self) -> None:
        """Impacts:
        _prompts

        Depends on:
        _prompt_template_names
        _llm
        _source_language
        _target_language
        _target_version
        """
        self._prompts = []
        for template in self._prompt_template_names:
            self._prompts.append(
                MODEL_PROMPT_ENGINES[self._llm.short_model_id](
                    source_language=self._source_language,
                    prompt_template=template,
                    target_language=self._target_language,
                    target_version=self._target_version,
                ).prompt
            )

    def _get_translation_chain(self) -> Runnable:
        prompt = self._prompts[0]
        translation_chain = RunnableParallel(
            prompt_value=lambda x, prompt=prompt: prompt.invoke(x),
            original_inputs=RunnablePassthrough(),
        ) | RunnableParallel(
            completion=lambda x: self._llm.invoke(x["prompt_value"]),
            original_inputs=itemgetter("original_inputs"),
            prompt_value=itemgetter("prompt_value"),
        )
        for prompt in self._prompts[1:]:
            translation_chain = (
                translation_chain
                | RunnableParallel(
                    prompt_value=lambda x, prompt=prompt: prompt.invoke(
                        dict(completion=x["completion"], **x["original_inputs"])
                    ),
                    original_inputs=itemgetter("original_inputs"),
                )
                | RunnableParallel(
                    completion=lambda x: self._llm.invoke(x["prompt_value"]),
                    original_inputs=itemgetter("original_inputs"),
                    prompt_value=itemgetter("prompt_value"),
                )
            )

        return translation_chain

    def _get_refiner_chain(self) -> Runnable:
        if len(self._refiner_types) == 0:
            return RunnableLambda(
                lambda x: self._parser.parse(x["completion"])  # type: ignore
            )

        refiner_type = self._refiner_types[0]
        if len(self._refiner_types) == 1:
            return RunnableLambda(
                lambda x, refiner_type=refiner_type: refiner_type(
                    llm=self._llm,
                    parser=self._parser,
                    max_retries=self._max_prompts,
                ).parse_completion(  # type: ignore
                    **x
                )
            )

        refiner_chain = RunnableParallel(
            completion=lambda x, refiner_type=refiner_type: refiner_type(
                llm=self._llm,
                parser=self._base_parser,
                max_retries=self._max_prompts,
            ).parse_completion(
                **x  # type: ignore
            ),
            prompt_value=itemgetter("prompt_value"),
        )
        for refiner_type in self._refiner_types[1:-1]:
            # NOTE: Do NOT remove refiner_type=refiner_type from lambda.
            # Due to lambda capture, must be present or chain will not
            # be correctly constructed.
            refiner_chain = refiner_chain | RunnableParallel(
                completion=lambda x, refiner_type=refiner_type: refiner_type(
                    llm=self._llm,
                    parser=self._base_parser,
                    max_retries=self._max_prompts,
                ).parse_completion(
                    **x  # type: ignore
                ),
                prompt_value=itemgetter("prompt_value"),
            )
        return refiner_chain | RunnableLambda(
            lambda x: self._refiner_types[-1](
                llm=self._llm,
                parser=self._parser,
                max_retries=self._max_prompts,
            ).parse_completion(
                **x
            )  # type: ignore
        )

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
        )

    def _load_chain(self):
        """Impacts:
        _chain

        Depends on:
        _parser
        _retriever
        _prompts
        _llm
        _source_language
        _refiner_types
        _max_prompts
        _base_parser
        """
        self._chain = (
            self._input_runnable()
            | self._get_translation_chain()
            | self._get_refiner_chain()
        )

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
        self._load_parameters()

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
                self._combine_blocks(out_block)
            else:
                out_block = self.translate_file(in_path, fail_path)
                self._combine_block(out_block)

            total_cost += out_block.total_cost
            log.info(f"Current Running Cost: {total_cost}")

            # For files where translation failed, write to failure path instead
            if not out_block.translation_completed:
                if fail_path is not None:
                    self._save_to_file(out_block, fail_path)
                continue

            if (
                collection_name is not None
                and self._vectorizer is not None
                and isinstance(out_block, TranslatedCodeBlock)
            ):
                self._vectorizer.add_nodes_recursively(
                    out_block,
                    collection_name,
                    in_path.name,
                )

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            if out_path is not None and (overwrite or not out_path.exists()):
                self._save_to_file(out_block, out_path)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def translate_blocks(
        self,
        block_collection: BlockCollection,
        failure_path: Path | None = None,
    ) -> TranslatedBlockCollection:
        self._load_parameters()
        input_blocks = list(block_collection.blocks)

        # Filter out blocks that don't match the input type or label
        if self._input_types is not None:
            input_blocks = [b for b in input_blocks if b.block_type in self._input_types]
        if self._input_labels is not None:
            input_blocks = [
                b for b in input_blocks if b.block_label in self._input_labels
            ]

        output_blocks = [self.translate_block(b, failure_path) for b in input_blocks]
        return TranslatedBlockCollection(
            blocks=output_blocks,
            previous_generations=block_collection.previous_generations,
        )

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
        self._load_parameters()
        input_block = self._split_file(file)
        return self.translate_block(input_block, failure_path)

    def translate_janus_file(
        self, file: Path, failure_path: Path | None = None
    ) -> TranslatedBlockCollection:
        self._load_parameters()
        with open(file, "r") as f:
            file_obj: JanusOutputObject = json.load(f)
        return self._translate_janus_obj(file_obj, failure_path)

    def _translate_janus_obj(
        self, obj: JanusOutputObject, failure_path: Path | None = None
    ) -> TranslatedBlockCollection:
        translated_block_collection = TranslatedBlockCollection.from_janus_object(obj)
        block_collection = translated_block_collection.to_block_collection()
        return self.translate_blocks(block_collection, failure_path)

    def translate_text(
        self, text: str, name: str, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        """
        Translates given text
        Arguments:
            text: text to translate
            name: the name of the text (filename if from a file)
            failure_path: path to write failure file if translation is not successful
        """
        self._load_parameters()
        input_block = self._split_text(text, name)
        return self.translate_block(input_block, failure_path)

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
        translation_successful = False
        last_prog, prog_delta = 0, 0.1
        stack = [translated_root]
        try:
            while stack:
                translated_block = stack.pop()
                stack.extend(translated_block.children)

                self._add_translation(translated_block)
                progress = translated_root.translation_completeness
                if progress - last_prog > prog_delta:
                    last_prog = int(progress / prog_delta) * prog_delta
                    log.info(f"[{root.name}] progress: {progress:.2%}")
        except EmptyTreeError:
            log.warning("Input file has no nodes of interest, skipping")
        except TokenLimitError:
            log.error("Ran into irreducible node too large for context, skipping")
        except FileSizeError:
            log.error("Current tile is too large for basic splitter, skipping")
        except OutputParserException as e:
            log.error(f"Skipping file, failed to parse output: {e}")
        except RateLimitError:
            log.error("Hit rate limit, skipping file")
        except BadRequestError as e:
            if str(e).startswith("Detected an error in the prompt"):
                log.warning("Malformed input, skipping")
            raise e
        except ValidationError as e:
            # Only allow ValidationError to pass if token limit is manually set
            if self._override_token_limit:
                log.warning(
                    "Current file and manually set token "
                    "limit is too large for this model, skipping"
                )
            else:
                raise e
        except ValueError as e:
            if str(e).startswith(
                "Error raised by bedrock service"
            ) and "maximum context length" in str(e):
                log.warning(
                    "Input is too large for this model's context length, skipping"
                )
            else:
                raise e
        else:
            translation_successful = True
        finally:
            out_obj = self._get_output_obj(
                translated_root, self._combine_output, include_previous_outputs=True
            )
            log.debug(f"Resulting Block:" f"{json.dumps(out_obj)}")
            if not translation_successful:
                translated_root.translated = False
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
        with get_model_callback() as cb:
            try:
                t0 = time.time()
                block.text = self._run_chain(block)
            except JanusParserException as e:
                block.text = e.unparsed_output
                block.tokens = self._llm.get_num_tokens(block.text) if block.text else 0
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
        self._load_parameters()
        return self._chain.invoke(block.original)

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | TranslatedBlockCollection | JanusOutputObject,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> JanusOutputObject:
        if isinstance(block, dict):
            # output object has already been generated
            new_block = deepcopy(block)
            if "intermediate_outputs" in new_block and not include_previous_outputs:
                del new_block["intermediate_outputs"]
            elif include_previous_outputs and "intermediate_outputs" not in new_block:
                new_block["intermediate_outputs"] = []
            return new_block

        janus_obj = block.to_janus_object(combine_children)
        if not include_previous_outputs:
            del janus_obj["intermediate_outputs"]

        if not (combine_children and block.translation_completed):
            return janus_obj

        # Parse combined output if output was combined
        if isinstance(block, TranslatedBlockCollection):
            for obj in janus_obj["outputs"]:
                if not isinstance(obj, dict):
                    continue
                out_str: str = obj["outputs"][0]  # type: ignore
                obj["outputs"] = [self._parser.parse_combined_output(out_str)]

        elif isinstance(block, TranslatedCodeBlock):
            out_str: str = janus_obj["outputs"][0]  # type: ignore
            janus_obj["outputs"] = [self._parser.parse_combined_output(out_str)]

        return janus_obj

    def _save_to_file(
        self, translation: TranslatedCodeBlock | TranslatedBlockCollection, out_path: Path
    ) -> None:
        """Save a file to disk.

        Arguments:
            block: The `TranslatedCodeBlock` to save to a file.
        """
        obj = self._get_output_obj(
            translation,
            combine_children=self._combine_output,
            include_previous_outputs=True,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

    def _combine_blocks(self, blocks: TranslatedBlockCollection) -> None:
        for b in blocks.blocks:
            self._combine_block(b)

    def _combine_block(self, block: TranslatedCodeBlock) -> None:
        if self._combine_output:
            self._combiner.combine(block)
            block.original.rebuild_text_from_children()

    def __or__(self, other: "Converter") -> ConverterChain:
        return ConverterChain(converters=[self, other])

    @property
    def source_language(self):
        return self._source_language

    @property
    def target_language(self):
        return self._target_language

    @property
    def target_version(self):
        return self._target_version

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
