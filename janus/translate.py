import json
import math
import re
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from openai import BadRequestError, RateLimitError
from text_generation.errors import ValidationError

from janus.language.naive.registry import CUSTOM_SPLITTERS

from .converter import Converter, run_if_changed
from .embedding.vectorize import ChromaDBVectorizer
from .language.block import CodeBlock, TranslatedCodeBlock
from .language.combine import ChunkCombiner, Combiner, JsonCombiner
from .language.splitter import EmptyTreeError, TokenLimitError
from .llm import load_model
from .llm.model_callbacks import get_model_callback
from .llm.models_info import MODEL_PROMPT_ENGINES
from .parsers.code_parser import CodeParser, GenericParser
from .parsers.doc_parser import MadlibsDocumentationParser, MultiDocumentationParser
from .parsers.eval_parser import EvaluationParser
from .parsers.reqs_parser import RequirementsParser
from .prompts.prompt import SAME_OUTPUT, TEXT_OUTPUT
from .utils.enums import LANGUAGES
from .utils.logger import create_logger

log = create_logger(__name__)


PARSER_TYPES: set[str] = {"code", "text", "eval", "madlibs", "multidoc", "requirements"}


class Translator(Converter):
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo-0125",
        model_arguments: dict[str, Any] = {},
        source_language: str = "fortran",
        target_language: str = "python",
        target_version: str | None = "3.10",
        max_prompts: int = 10,
        max_tokens: int | None = None,
        prompt_template: str | Path = "simple",
        parser_type: str = "code",
        db_path: str | None = None,
        db_config: dict[str, Any] | None = None,
        custom_splitter: str | None = None,
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            max_tokens: The maximum number of tokens the model will take in.
                If unspecificed, model's default max will be used.
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are "code" (default), "text", and "eval".
        """
        self._custom_splitter = custom_splitter
        super().__init__(source_language=source_language)

        self._parser_type: str | None
        self._model_name: str | None
        self._custom_model_arguments: dict[str, Any] | None
        self._target_language: str | None
        self._target_version: str | None
        self._target_glob: str | None
        self._prompt_template_name: str | None
        self._db_path: str | None
        self._db_config: dict[str, Any] | None

        self._llm: BaseLanguageModel | None
        self._parser: BaseOutputParser | None
        self._combiner: Combiner | None
        self._prompt: ChatPromptTemplate | None

        self.max_prompts = max_prompts
        self.override_token_limit = False if max_tokens is None else True
        self._max_tokens = max_tokens

        self.set_model(model_name=model, **model_arguments)
        self.set_parser_type(parser_type=parser_type)
        self.set_prompt(prompt_template=prompt_template)
        self.set_target_language(
            target_language=target_language,
            target_version=target_version,
        )
        self.set_db_path(db_path=db_path)
        self.set_db_config(db_config=db_config)

        self._load_parameters()

    def _load_parameters(self) -> None:
        self._load_model()
        self._load_prompt()
        self._load_parser()
        self._load_combiner()
        self._load_vectorizer()
        super()._load_parameters()  # will call self._changed_attrs.clear()

    def translate(
        self,
        input_directory: str | Path,
        output_directory: str | Path | None = None,
        overwrite: bool = False,
        collection_name: str | None = None,
    ) -> None:
        """Translate code in the input directory from the source language to the target
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

        source_suffix = LANGUAGES[self._source_language]["suffix"]
        target_suffix = LANGUAGES[self._target_language]["suffix"]

        input_paths = [p for p in input_directory.rglob(self._source_glob)]

        log.info(f"Input directory: {input_directory.absolute()}")
        log.info(
            f"{self._source_language.capitalize()} '*.{source_suffix}' files: "
            f"{len(input_paths)}"
        )
        log.info(
            "Other files (skipped): "
            f"{len(list(input_directory.iterdir())) - len(input_paths)}\n"
        )
        if output_directory is not None:
            output_paths = [
                output_directory
                / p.relative_to(input_directory).with_suffix(f".{target_suffix}")
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
                    f"'*.{source_suffix}' files"
                )
        else:
            in_out_pairs = [(f, None) for f in input_paths]
        log.info(f"Translating {len(in_out_pairs)} '*.{source_suffix}' files")

        # Now, loop through every code block in every file and translate it with an LLM
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
                        "limit is too large for this model"
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

            # Don't attempt to write files for which translation failed
            if not out_block.translated:
                continue

            # # maybe want target embeddings?
            # if self.outputting_requirements():
            #     filename = str(relative)
            #     embedding_type = EmbeddingType.REQUIREMENT
            # elif self.outputting_summary():
            #     filename = str(relative)
            #     embedding_type = EmbeddingType.SUMMARY
            # elif self.outputting_pseudocode():
            #     filename = out_path.name
            #     embedding_type = EmbeddingType.PSEUDO
            # else:
            #     filename = out_path.name
            #     embedding_type = EmbeddingType.TARGET
            #
            # self._embed_nodes_recursively(out_block, embedding_type, filename)

            if collection_name is not None:
                self._vectorizer.add_nodes_recursively(
                    out_block,
                    collection_name,
                    in_path.name,
                )
                # out_text = self.parser.parse_combined_output(out_block.complete_text)
                # # Using same id naming convention from vectorize.py
                # ids = [str(uuid.uuid3(uuid.NAMESPACE_DNS, out_text))]
                # output_collection.upsert(ids=ids, documents=[out_text])

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            self._combiner.combine(out_block)
            if out_path is not None and (overwrite or not out_path.exists()):
                self._save_to_file(out_block, out_path)

        log.info(f"Total cost: ${total_cost:,.2f}")

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

    def outputting_requirements(self) -> bool:
        """Is the output of the translator a requirements file?"""
        # expect we will revise system to output more than a single output
        # so this is placeholder logic
        return self._prompt_template_name == "requirements"

    def outputting_summary(self) -> bool:
        """Is the output of the translator a summary documentation?"""
        return self._prompt_template_name == "document"

    def outputting_pseudocode(self) -> bool:
        """Is the output of the translator pseudocode?"""
        # expect we will revise system to output more than a single output
        # so this is placeholder logic
        return self._prompt_template_name == "pseudocode"

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

    def _run_chain(self, block: TranslatedCodeBlock) -> str:
        """Run the model with three nested error fixing schemes.
        First, try to fix simple formatting errors by giving the model just
        the output and the parsing error. After a number of attempts, try
        giving the model the output, the parsing error, and the original
        input. Again check/retry this output to solve for formatting errors.
        If we still haven't succeeded after several attempts, the model may
        be getting thrown off by a bad initial output; start from scratch
        and try again.

        The number of tries for each layer of this scheme is roughly equal
        to the cube root of self.max_retries, so the total calls to the
        LLM will be roughly as expected (up to sqrt(self.max_retries) over)
        """
        self._parser.set_reference(block.original)

        # Retries with just the output and the error
        n1 = round(self.max_prompts ** (1 / 3))

        # Retries with the input, output, and error
        n2 = round((self.max_prompts // n1) ** (1 / 2))

        # Retries with just the input
        n3 = math.ceil(self.max_prompts / (n1 * n2))

        fix_format = OutputFixingParser.from_llm(
            llm=self._llm,
            parser=self._parser,
            max_retries=n1,
        )
        retry = RetryWithErrorOutputParser.from_llm(
            llm=self._llm,
            parser=fix_format,
            max_retries=n2,
        )

        completion_chain = self._prompt | self._llm
        chain = RunnableParallel(
            completion=completion_chain, prompt_value=self._prompt
        ) | RunnableLambda(lambda x: retry.parse_with_prompt(**x))

        for _ in range(n3):
            try:
                return chain.invoke({"SOURCE_CODE": block.original.text})
            except OutputParserException:
                pass

        raise OutputParserException(f"Failed to parse after {n1*n2*n3} retries")

    def _save_to_file(self, block: CodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        # TODO: can't use output fixer and this system for combining output
        out_text = self._parser.parse_combined_output(block.complete_text)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text, encoding="utf-8")

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

    def set_prompt(self, prompt_template: str | Path) -> None:
        """Validate and set the prompt template name.

        The affected objects will not be updated until translate() is called.

        Arguments:
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        self._prompt_template_name = prompt_template

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
        self._target_glob = f"**/*.{LANGUAGES[target_language]['suffix']}"
        self._target_language = target_language
        self._target_version = target_version

    def set_db_path(self, db_path: str) -> None:
        self._db_path = db_path

    def set_db_config(self, db_config: dict[str, Any] | None) -> None:
        self._db_config = db_config

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
        self._llm, token_limit, self.model_cost = load_model(self._model_name)
        # Set the max_tokens to less than half the model's limit to allow for enough
        # tokens at output
        # Only modify max_tokens if it is not specified by user
        if not self.override_token_limit:
            self._max_tokens = token_limit // 2.5

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
        if (
            self._parser_type in {"eval", "multidoc", "madlibs"}
            and "json" != self._target_language
        ):
            raise ValueError(
                f"Parser type ({self._parser_type}) suggests target language"
                f" should be 'json', but is '{self._target_language}'"
            )
        if "code" == self._parser_type:
            self._parser = CodeParser(language=self._target_language)
        elif "eval" == self._parser_type:
            self._parser = EvaluationParser()
        elif "multidoc" == self._parser_type:
            self._parser = MultiDocumentationParser()
        elif "madlibs" == self._parser_type:
            self._parser = MadlibsDocumentationParser()
        elif "text" == self._parser_type:
            self._parser = GenericParser()
        elif "requirements" == self._parser_type:
            self._parser = RequirementsParser()
        else:
            raise ValueError(
                f"Unsupported parser type: {self._parser_type}. Can be: "
                f"{PARSER_TYPES}"
            )

    @run_if_changed(
        "_prompt_template_name",
        "_source_language",
        "_target_language",
        "_target_version",
        "_model_name",
    )
    def _load_prompt(self) -> None:
        """Load the prompt according to this instance's attributes.

        If the relevant fields have not been changed since the last time this
        method was called, nothing happens.
        """
        if self._prompt_template_name in SAME_OUTPUT:
            if self._target_language != self._source_language:
                raise ValueError(
                    f"Prompt template ({self._prompt_template_name}) suggests "
                    f"source and target languages should match, but do not "
                    f"({self._source_language} != {self._target_language})"
                )
        if self._prompt_template_name in TEXT_OUTPUT and self._target_language != "text":
            raise ValueError(
                f"Prompt template ({self._prompt_template_name}) suggests target "
                f"language should be 'text', but is '{self._target_language}'"
            )

        prompt_engine = MODEL_PROMPT_ENGINES[self._model_name](
            source_language=self._source_language,
            target_language=self._target_language,
            target_version=self._target_version,
            prompt_template=self._prompt_template_name,
        )
        self._prompt = prompt_engine.prompt

    @run_if_changed("_db_path")
    def _load_vectorizer(self) -> None:
        if self._db_path is None:
            self._vectorizer = None
            return
        vectorizer_factory = ChromaDBVectorizer()
        self._vectorizer = vectorizer_factory.create_vectorizer(
            self._db_path, self._db_config
        )

    @run_if_changed(
        "_source_language",
        "_max_tokens",
        "_llm",
        "_protected_node_types",
        "_prune_node_types",
    )
    def _load_splitter(self) -> None:
        if self._custom_splitter is None:
            super()._load_splitter()
        else:
            kwargs = dict(
                max_tokens=self._max_tokens,
                model=self._llm,
                protected_node_types=self._protected_node_types,
                prune_node_types=self._prune_node_types,
            )
            # TODO: This should be configurable
            if self._custom_splitter == "tag":
                kwargs["tag"] = "<ITMOD_ALC_SPLIT>"
            self._splitter = CUSTOM_SPLITTERS[self._custom_splitter](
                language=self._source_language, **kwargs
            )

    @run_if_changed("_target_language", "_parser_type")
    def _load_combiner(self) -> None:
        if self._parser_type == "requirements":
            self._combiner = ChunkCombiner()
        elif self._target_language == "json":
            self._combiner = JsonCombiner()
        else:
            self._combiner = Combiner()


class Documenter(Translator):
    def __init__(
        self, source_language: str = "fortran", drop_comments: bool = True, **kwargs
    ):
        kwargs.update(
            source_language=source_language,
            target_language="text",
            target_version=None,
            prompt_template="document",
            parser_type="text",
        )
        super().__init__(**kwargs)

        if drop_comments:
            comment_node_type = LANGUAGES[source_language].get(
                "comment_node_type", "comment"
            )
            self.set_prune_node_types([comment_node_type])


class MultiDocumenter(Documenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_prompt("multidocument")
        self.set_parser_type("multidoc")
        self.set_target_language("json", None)


class MadLibsDocumenter(Documenter):
    def __init__(
        self,
        comments_per_request: int | None = None,
        **kwargs,
    ) -> None:
        kwargs.update(drop_comments=False)
        super().__init__(**kwargs)
        self.set_prompt("document_madlibs")
        self.set_parser_type("madlibs")
        self.set_target_language("json", None)
        self.comments_per_request = comments_per_request

    def _add_translation(self, block: TranslatedCodeBlock):
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self.comments_per_request is None:
            return super()._add_translation(block)

        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>"
        comments = list(
            re.finditer(
                comment_pattern,
                block.original.text,
            )
        )

        if not comments:
            log.info(f"[{block.name}] Skipping commentless block")
            block.translated = True
            block.text = None
            block.complete = True
            return

        if len(comments) <= self.comments_per_request:
            return super()._add_translation(block)

        comment_group_indices = list(range(0, len(comments), self.comments_per_request))
        log.debug(
            f"[{block.name}] Block contains more than {self.comments_per_request}"
            f" comments, splitting {len(comments)} comments into"
            f" {len(comment_group_indices)} groups"
        )

        block.processing_time = 0
        block.cost = 0
        block.retries = 0
        obj = {}
        for i in range(0, len(comments), self.comments_per_request):
            # Split the text into the section containing comments of interest,
            #  all the text prior to those comments, and all the text after them
            working_comments = comments[i : i + self.comments_per_request]
            start_idx = working_comments[0].start()
            end_idx = working_comments[-1].end()
            prefix = block.original.text[:start_idx]
            keeper = block.original.text[start_idx:end_idx]
            suffix = block.original.text[end_idx:]

            # Strip all comment placeholders outside of the section of interest
            prefix = re.sub(comment_pattern, "", prefix)
            suffix = re.sub(comment_pattern, "", suffix)

            # Build a new TranslatedBlock using the new working text
            working_copy = deepcopy(block.original)
            working_copy.text = prefix + keeper + suffix
            working_block = TranslatedCodeBlock(working_copy, self._target_language)

            # Run the LLM on the working text
            super()._add_translation(working_block)

            # Update metadata to include for all runs
            block.retries += working_block.retries
            block.cost += working_block.cost
            block.processing_time += working_block.processing_time

            # Update the output text to merge this section's output in
            out_text = self._parser.parse(working_block.text)
            obj.update(json.loads(out_text))

        self._parser.set_reference(block.original)
        block.text = self._parser.parse(json.dumps(obj))
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

    def _get_obj(
        self, block: TranslatedCodeBlock
    ) -> dict[str, int | float | dict[str, str]]:
        out_text = self._parser.parse_combined_output(block.complete_text)
        obj = dict(
            retries=block.total_retries,
            cost=block.total_cost,
            processing_time=block.processing_time,
            comments=json.loads(out_text),
        )
        return obj

    def _save_to_file(self, block: TranslatedCodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        obj = self._get_obj(block)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


class DiagramGenerator(Documenter):
    """DiagramGenerator

    A class that translates code from one programming language to a set of diagrams.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo-0125",
        model_arguments: dict[str, Any] = {},
        source_language: str = "fortran",
        max_prompts: int = 10,
        db_path: str | None = None,
        db_config: dict[str, Any] | None = None,
        diagram_type="Activity",
        add_documentation=False,
        custom_splitter: str | None = None,
    ) -> None:
        """Initialize the DiagramGenerator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            db_path: path to chroma database
            db_config: database configuraiton
            diagram_type: type of PLANTUML diagram to generate
        """
        super().__init__(
            model=model,
            model_arguments=model_arguments,
            source_language=source_language,
            max_prompts=max_prompts,
            db_path=db_path,
            db_config=db_config,
            custom_splitter=custom_splitter,
        )
        self._diagram_type = diagram_type
        self._add_documentation = add_documentation
        self._documenter = None
        self._model = model
        self._model_arguments = model_arguments
        self._max_prompts = max_prompts
        if add_documentation:
            self._diagram_prompt_template_name = "diagram_with_documentation"
        else:
            self._diagram_prompt_template_name = "diagram"
        self._load_diagram_prompt_engine()

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

        if self._add_documentation:
            documentation_block = deepcopy(block)
            super()._add_translation(documentation_block)
            if not documentation_block.translated:
                message = "Error: unable to produce documentation for code block"
                log.message(message)
                raise ValueError(message)
            documentation = json.loads(documentation_block.text)["docstring"]

        if self._llm is None:
            message = (
                "Model not configured correctly, cannot translate. Try setting "
                "the model"
            )
            log.error(message)
            raise ValueError(message)

        log.debug(f"[{block.name}] Translating...")
        log.debug(f"[{block.name}] Input text:\n{block.original.text}")

        self._parser.set_reference(block.original)

        query_and_parse = self.diagram_prompt | self._llm | self._parser

        if self._add_documentation:
            block.text = query_and_parse.invoke(
                {
                    "SOURCE_CODE": block.original.text,
                    "DIAGRAM_TYPE": self._diagram_type,
                    "DOCUMENTATION": documentation,
                }
            )
        else:
            block.text = query_and_parse.invoke(
                {
                    "SOURCE_CODE": block.original.text,
                    "DIAGRAM_TYPE": self._diagram_type,
                }
            )
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(f"[{block.name}] Output code:\n{block.text}")

    @run_if_changed(
        "_diagram_prompt_template_name",
        "_source_language",
    )
    def _load_diagram_prompt_engine(self) -> None:
        """Load the prompt engine according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        if self._diagram_prompt_template_name in SAME_OUTPUT:
            if self._target_language != self._source_language:
                raise ValueError(
                    f"Prompt template ({self._prompt_template_name}) suggests "
                    f"source and target languages should match, but do not "
                    f"({self._source_language} != {self._target_language})"
                )
        if (
            self._diagram_prompt_template_name in TEXT_OUTPUT
            and self._target_language != "text"
        ):
            raise ValueError(
                f"Prompt template ({self._prompt_template_name}) suggests target "
                f"language should be 'text', but is '{self._target_language}'"
            )

        self._diagram_prompt_engine = MODEL_PROMPT_ENGINES[self._model_name](
            source_language=self._source_language,
            target_language=self._target_language,
            target_version=self._target_version,
            prompt_template=self._diagram_prompt_template_name,
        )
        self.diagram_prompt = self._diagram_prompt_engine.prompt


class RequirementsDocumenter(Documenter):
    """RequirementsGenerator

    A class that translates code from one programming language to its requirements.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_prompt("chunk_requirements")
        self.set_target_language("json", None)
        self.set_parser_type("requirements")

    def _save_to_file(self, block: TranslatedCodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        output_list = list()
        # For each chunk of code, get generation metadata, the text of the code,
        # and the LLM generated requirements
        for child in block.children:
            code = child.original.text
            requirements = self._parser.parse_combined_output(child.complete_text)
            metadata = dict(
                retries=child.total_retries,
                cost=child.total_cost,
                processing_time=child.processing_time,
            )
            # Put them all in a top level 'output' key
            output_list.append(
                dict(metadata=metadata, code=code, requirements=requirements)
            )
        obj = dict(
            output=output_list,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
