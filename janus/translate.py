import functools
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Set

from langchain.callbacks import get_openai_callback
from langchain.schema.vectorstore import VectorStore

from .language.block import CodeBlock, TranslatedCodeBlock
from .language.combine import Combiner
from .language.mumps import MumpsSplitter
from .language.splitter import Splitter
from .language.treesitter import TreeSitterSplitter
from .llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS, TOKEN_LIMITS
from .llm.embeddings import Embeddings, get_embeddings_factory
from .parsers.code_parser import PARSER_TYPES, CodeParser, EvaluationParser, JanusParser
from .prompts.prompt import SAME_OUTPUT, TEXT_OUTPUT, PromptEngine
from .utils.enums import CUSTOM_SPLITTERS, LANGUAGES, EmbeddingType
from .utils.logger import create_logger

log = create_logger(__name__)

VALID_MODELS: Set[str] = set(MODEL_CONSTRUCTORS).intersection(MODEL_DEFAULT_ARGUMENTS)


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


class Translator:
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_arguments: Dict[str, Any] = {},
        embeddings_override: Embeddings = None,
        source_language: str = "fortran",
        target_language: str = "python",
        target_version: str = "3.10",
        max_prompts: int = 10,
        prompt_template: str | Path = "simple",
        parser_type: str = "code",
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            embeddings_override: Hard-code the embeddings rather than picking one
                based on the model. Leave as None to be based on model.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
            parser_type: The type of parser to use for parsing the LLM output. Valid
                values are "code" (default), "text", and "eval".
        """
        self._changed_attrs: set = set()

        self._parser_type: Optional[str]
        self._model_name: Optional[str]
        self._custom_model_arguments: Optional[Dict[str, Any]]
        self._embeddings_override: Optional[Embeddings]
        self._source_language: Optional[str]
        self._source_glob: Optional[str]
        self._target_language: Optional[str]
        self._target_version: Optional[str]
        self._target_glob: Optional[str]
        self._prompt_template_name: Optional[str]
        self._parser: Optional[JanusParser]
        self._splitter: Optional[Splitter]

        self._combiner: Combiner = Combiner()

        self.set_model(model_name=model, **model_arguments)
        self.set_embeddings(embeddings_override=embeddings_override)
        self.set_prompt(prompt_template=prompt_template)
        self.set_parser_type(parser_type=parser_type)
        self.set_source_language(source_language=source_language)
        self.set_target_language(
            target_language=target_language, target_version=target_version
        )

        self._load_parameters()

        self.max_prompts = max_prompts

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
        self._load_prompt_engine()
        self._load_splitter()
        self._load_parser()
        self._load_embeddings()
        self._changed_attrs.clear()

    def translate(
        self,
        input_directory: str | Path,
        output_directory: str | Path,
        overwrite: bool = False,
    ) -> None:
        """Translate code in the input directory from the source language to the target
        language, and write the resulting files to the output directory.

        Arguments:
            input_directory: The directory containing the code to translate.
            output_directory: The directory to write the translated code to.
            overwrite: Whether to overwrite existing files (vs skip them)
        """
        # Convert paths to pathlib Paths if needed
        if isinstance(input_directory, str):
            input_directory = Path(input_directory)
        if isinstance(output_directory, str):
            output_directory = Path(output_directory)

        # Make sure the output directory exists
        if not output_directory.exists():
            output_directory.mkdir(parents=True)

        target_suffix = LANGUAGES[self._target_language]["suffix"]

        input_paths = input_directory.rglob(self._source_glob)

        # Now, loop through every code block in every file and translate it with an LLM
        total_cost = 0.0
        for in_path in input_paths:
            relative = in_path.relative_to(input_directory)
            out_path = output_directory / relative.with_suffix(f".{target_suffix}")
            if out_path.exists() and not overwrite:
                continue

            # Track the cost of translating the file
            #  TODO: If non-OpenAI models with prices are added, this will need
            #   to be updated.
            with get_openai_callback() as cb:
                out_block = self.translate_file(in_path)
                total_cost += cb.total_cost

            # Don't attempt to write files for which translation failed
            if not out_block.translated:
                continue

            # maybe want target embeddings?
            if self.outputting_requirements():
                filename = str(relative)
                embedding_type = EmbeddingType.REQUIREMENT
            elif self.outputting_summary():
                filename = str(relative)
                embedding_type = EmbeddingType.SUMMARY
            else:
                filename = out_path.name
                embedding_type = EmbeddingType.TARGET

            self._embed_nodes_recursively(out_block, embedding_type, filename)

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            self._combiner.combine(out_block)
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
        log.info(f"[{filename}] Splitting file")
        input_block = self.splitter.split(file)
        log.info(
            f"[{filename}] File split into {input_block.n_descendents:,} blocks, "
            f"tree of height {input_block.height}"
        )
        log.info(f"[{filename}] Input CodeBlock Structure:\n{input_block.tree_str()}")
        self._embed_nodes_recursively(input_block, EmbeddingType.SOURCE, filename)
        output_block = self._iterative_translate(input_block)
        if output_block.translated:
            completeness = output_block.translation_completeness
            log.info(
                f"[{filename}] Translation complete\n"
                f"  {completeness:.2%} of input successfully translated\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
            )
        else:
            log.error(
                f"[{filename}] Translation failed\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
            )
        return output_block

    def embeddings(self, embedding_type: EmbeddingType) -> VectorStore:
        """Get the Chroma vector store for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to get the vector store for

        Returns:
            The Chroma vector store for the given embedding type
        """
        return self._collections[embedding_type]

    def _embed_nodes_recursively(
        self, code_block: CodeBlock, embedding_type: EmbeddingType, file_name: str
    ) -> None:
        """Embed all nodes in the tree rooted at `code_block`

        Arguments:
            code_block: CodeBlock to embed
            embedding_type: EmbeddingType to use
            file_name: Name of file containing `code_block`
        """
        nodes = [code_block]
        while nodes:
            node = nodes.pop(0)
            self._embed(node, embedding_type, file_name)
            nodes.extend(node.children)

    def _embed(
        self,
        code_block: CodeBlock,
        embedding_type: EmbeddingType,
        file_name: str  # perhaps this should be a relative path from the source, but for
        # now we're all in 1 directory
    ) -> bool:
        """Calculate code_block embedding, returning success & storing in embedding_id

        Arguments:
            code_block: CodeBlock to embed
            embedding_type: EmbeddingType to use
            file_name: Name of file containing `code_block`

        Returns:
            True if embedding was successful, False otherwise
        """
        if code_block.text:
            metadatas = [
                {
                    "type": code_block.type,
                    "original_filename": file_name,
                    "tokens": code_block.tokens,
                    "cost": 0,  # TranslatedCodeBlock has cost
                },
            ]
            # for now, dealing with missing metadata by skipping it
            if code_block.text is not None:
                metadatas[0]["hash"] = hash(code_block.text)
            if code_block.start_point is not None:
                metadatas[0]["start_line"] = code_block.start_point[0]
            if code_block.end_point is not None:
                metadatas[0]["end_line"] = code_block.end_point[0]
            the_text = [code_block.text]
            code_block.embedding_id = self._add_text_to_vector_store(
                embedding_type, the_text, metadatas
            )
            return True
        return False

    def _add_text_to_vector_store(self, embedding_type, texts, metadatas):
        """Helper function that stores a single text (in an array) and associated
        metadatas, returning the embedding id"""
        vector_store = self.embeddings(embedding_type)
        return vector_store.add_texts(texts, metadatas)[0]

    def outputting_requirements(self) -> bool:
        """Is the output of the translator a requirements file?"""
        # expect we will revise system to output more than a single output
        # so this is placeholder logic
        return self._prompt_template_name == "requirements"

    def outputting_summary(self) -> bool:
        """Is the output of the translator a summary documentation?"""
        return self._prompt_template_name == "document"

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

            for child in translated_block.children:
                # Don't bother translating children if they aren't used
                if self._combiner.contains_child(translated_block.text, child):
                    stack.append(child)
                else:
                    log.warning(f"Skipping {child.id} (not referenced in parent code)")

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
        if model_name not in VALID_MODELS:
            raise ValueError(
                f"Invalid model: {model_name}. Valid models are: {VALID_MODELS}"
            )

        self._model_name = model_name
        self._custom_model_arguments = custom_arguments

    def set_embeddings(self, embeddings_override: Embeddings) -> None:
        """Validate and set the Embeddings factory.

        The affected objects will not be updated until translate() is called.

        Arguments:
            embeddings_override: Hard-code the embeddings rather than picking one
                based on the model. Leave as None to be based on model."""
        if not embeddings_override:
            self._embeddings_override = None
        elif not isinstance(embeddings_override, Embeddings):
            raise ValueError(f"Can't set Embeddings as type {type(embeddings_override)}")
        else:
            self._embeddings_override = embeddings_override

    def set_prompt(self, prompt_template: str | Path) -> None:
        """Validate and set the prompt template name.

        The affected objects will not be updated until translate() is called.

        Arguments:
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        self._prompt_template_name = prompt_template

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
                "Valid source languages are found in `janus.utils.enums.LANGUAGES`."
            )
        self._target_glob = f"**/*.{LANGUAGES[target_language]['suffix']}"
        self._target_language = target_language
        self._target_version = target_version

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

    @run_if_changed("_model_name", "_custom_model_arguments")
    def _load_model(self):
        """Load the model according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """

        # Get default arguments, set custom ones
        model_arguments = deepcopy(MODEL_DEFAULT_ARGUMENTS[self._model_name])
        model_arguments.update(self._custom_model_arguments)

        # Load the model
        self._llm = MODEL_CONSTRUCTORS[self._model_name](**model_arguments)
        self._max_tokens = TOKEN_LIMITS.get(self._model_name, 4096)

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

    @run_if_changed("_model_name", "_embeddings_override")
    def _load_embeddings(self) -> None:
        """Load the embeddings according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        # clean up
        if hasattr(self, "_collections"):
            for key in self._collections:
                self._embeddings.delete_collection(self._collections[key])

        if self._embeddings_override:
            self._embeddings = self._embeddings_override
        else:
            self._embeddings = get_embeddings_factory(self._llm)

        self._collections = {}
        for key in EmbeddingType:
            self._collections[key] = self._embeddings.create_collection(
                f"{key.name}-{id(self)}"
            )
