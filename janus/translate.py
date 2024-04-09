import re
from pathlib import Path
from typing import Any, Dict

from langchain_community.callbacks import get_openai_callback
from openai import BadRequestError, RateLimitError

from .converter import Converter, run_if_changed
from .embedding.vectorize import ChromaDBVectorizer
from .language.block import CodeBlock, TranslatedCodeBlock
from .language.splitter import EmptyTreeError, TokenLimitError
from .llm import load_model
from .parsers.code_parser import (
    PARSER_TYPES,
    CodeParser,
    EvaluationParser,
    JanusParser,
    MadlibsDocumentationParser,
)
from .prompts.prompt import SAME_OUTPUT, TEXT_OUTPUT, PromptEngine
from .utils.enums import LANGUAGES
from .utils.logger import create_logger

log = create_logger(__name__)


class Translator(Converter):
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_arguments: Dict[str, Any] = {},
        source_language: str = "fortran",
        target_language: str = "python",
        target_version: str | None = "3.10",
        max_prompts: int = 10,
        prompt_template: str | Path = "simple",
        parser_type: str = "code",
        db_path: str | None = None,
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
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are "code" (default), "text", and "eval".
        """
        super().__init__(source_language=source_language)

        self._parser_type: None | str
        self._parser: None | JanusParser
        self._model_name: None | str
        self._custom_model_arguments: None | Dict[str, Any]
        self._target_language: None | str
        self._target_version: None | str
        self._target_glob: None | str
        self._prompt_template_name: None | str
        self._db_path: None | str

        self.set_model(model_name=model, **model_arguments)
        self.set_parser_type(parser_type=parser_type)
        self.set_prompt(prompt_template=prompt_template)
        self.set_target_language(
            target_language=target_language,
            target_version=target_version,
        )
        self.set_db_path(db_path=db_path)

        self._load_parameters()

        self.max_prompts = max_prompts

    def _load_parameters(self) -> None:
        self._load_model()
        self._load_prompt_engine()
        self._load_parser()
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
            except BadRequestError as e:
                if str(e).startswith("Detected an error in the prompt"):
                    log.warning("Malformed input, skipping")
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
        output_block = self._iterative_translate(input_block)
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

            # Track the cost of translating this block
            #  TODO: If non-OpenAI models with prices are added, this will need
            #   to be updated.
            with get_openai_callback() as cb:
                self._add_translation(translated_block)
                translated_block.cost = cb.total_cost
                translated_block.retries = max(0, cb.successful_requests - 1)

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

        log.debug(f"[{block.name}] Translating...")
        log.debug(f"[{block.name}] Input text:\n{block.original.text}")
        prompt = self._prompt_engine.create(block.original)
        top_score = -1.0

        if self._llm is None:
            message = (
                "Model not configured correctly, cannot translate. Try setting "
                "the model"
            )
            log.error(message)
            raise ValueError(message)

        # Retry the request up to max_prompts times before failing
        for _ in range(self.max_prompts + 1):
            output = self._llm.predict_messages(prompt)
            try:
                parsed_output = self.parser.parse(output.content)
            except ValueError as e:
                log.warning(f"[{block.name}] Failed to parse output: {e}")
                log.debug(f"[{block.name}] Failed output:\n{output.content}")
                continue

            score = self.parser.score(block.original, parsed_output)
            if score > top_score:
                block.text = parsed_output
                top_score = score

            if score >= 1.0:
                break

        else:
            if block.text is None:
                error_msg = (
                    f"[{block.name}] Failed to parse output after "
                    f"{self.max_prompts} retries. Marking as untranslated."
                )
                log.warning(error_msg)
                return

            log.warning(f"[{block.name}] Output not complete")

        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(f"[{block.name}] Output code:\n{block.text}")

    def _save_to_file(self, block: CodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        out_text = self.parser.parse_combined_output(block.complete_text)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text, encoding="utf-8")

    def set_model(self, model_name: str, **custom_arguments: Dict[str, Any]):
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

    def set_target_language(self, target_language: str, target_version: str) -> None:
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

    @run_if_changed("_model_name", "_custom_model_arguments")
    def _load_model(self):
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
        self._max_tokens = token_limit // 2.5

    @run_if_changed("_parser_type", "_target_language")
    def _load_parser(self) -> None:
        """Load the parser according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        if "text" == self._target_language and self._parser_type not in {"text", "doc"}:
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
        elif "doc" == self._parser_type:
            self.parser = MadlibsDocumentationParser()
        elif "text" == self._parser_type:
            self.parser = JanusParser()
        else:
            raise ValueError(
                f"Unsupported parser type: {self._parser_type}. Can be: "
                f"{PARSER_TYPES}"
            )

    @run_if_changed(
        "_prompt_template_name", "_source_language", "_target_language", "_target_version"
    )
    def _load_prompt_engine(self) -> None:
        """Load the prompt engine according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
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

        self._prompt_engine = PromptEngine(
            source_language=self._source_language,
            target_language=self._target_language,
            target_version=self._target_version,
            prompt_template=self._prompt_template_name,
        )

    @run_if_changed("_db_path")
    def _load_vectorizer(self) -> None:
        if self._db_path is None:
            self._vectorizer = None
            return
        vectorizer_factory = ChromaDBVectorizer()
        self._vectorizer = vectorizer_factory.create_vectorizer(self._db_path)


class Documenter(Translator):
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_arguments: Dict[str, Any] = {},
        source_language: str = "fortran",
        max_prompts: int = 10,
        db_path: str | None = None,
        drop_comments: bool = False,
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(
            model=model,
            model_arguments=model_arguments,
            source_language=source_language,
            target_language="text",
            target_version=None,
            max_prompts=max_prompts,
            prompt_template="document",
            parser_type="text",
            db_path=db_path,
        )

        module_node_type = LANGUAGES[source_language]["functional_node_type"]
        self.set_protected_node_types([module_node_type])

        if drop_comments:
            comment_node_type = LANGUAGES[source_language]["comment_node_type"]
            self.set_prune_node_types([comment_node_type])

    def _split_file(self, file: Path) -> CodeBlock:
        filename = file.name
        log.info(f"[{filename}] Splitting file")
        root = self._splitter.split(file, prune_unprotected=True)
        log.info(
            f"[{filename}] File split into {root.n_descendents:,} blocks, "
            f"tree of height {root.height}"
        )
        log.info(f"[{filename}] Input CodeBlock Structure:\n{root.tree_str()}")
        return root


class MadLibsDocumenter(Translator):
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_arguments: Dict[str, Any] = {},
        source_language: str = "fortran",
        max_prompts: int = 10,
        db_path: str | None = None,
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(
            model=model,
            model_arguments=model_arguments,
            source_language=source_language,
            target_language="json",
            target_version=None,
            max_prompts=max_prompts,
            prompt_template="document_madlibs",
            parser_type="doc",
            db_path=db_path,
        )

    def _add_translation(self, block: TranslatedCodeBlock):
        if block.original.text:
            first_comment = re.search(
                r"<(?:INLINE|BLOCK)_COMMENT \w{8}>",
                block.original.text,
            )
            if first_comment is None:
                log.info(f"[{block.name}] Skipping commentless block")
                block.translated = True
                return

        super()._add_translation(block)
