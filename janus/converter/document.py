import json
import re
from copy import deepcopy

from janus.converter.converter import Converter
from janus.language.block import TranslatedCodeBlock
from janus.language.combine import JsonCombiner
from janus.parsers.doc_parser import (
    MadlibsDocumentationParser,
    MultiDocumentationParser,
)
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Documenter(Converter):
    def __init__(
        self, source_language: str = "fortran", drop_comments: bool = True, **kwargs
    ):
        kwargs.update(source_language=source_language)
        super().__init__(**kwargs)
        self.set_prompt("document")

        if drop_comments:
            comment_node_type = LANGUAGES[source_language].get(
                "comment_node_type", "comment"
            )
            self.set_prune_node_types((comment_node_type,))

        self._load_parameters()


class MultiDocumenter(Documenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_prompt("multidocument")
        self._combiner = JsonCombiner()
        self._parser = MultiDocumentationParser()


class MadLibsDocumenter(Documenter):
    def __init__(
        self,
        comments_per_request: int | None = None,
        **kwargs,
    ) -> None:
        kwargs.update(drop_comments=False)
        super().__init__(**kwargs)
        self.set_prompt("document_madlibs")
        self._combiner = JsonCombiner()
        self._parser = MadlibsDocumentationParser()

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

        self._parser.parse_input(block.original)
        block.text = self._parser.parse(json.dumps(obj))
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True
