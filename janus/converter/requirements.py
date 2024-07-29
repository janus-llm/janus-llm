import json
from pathlib import Path

from janus.converter.document import Documenter
from janus.language.block import TranslatedCodeBlock
from janus.language.combine import ChunkCombiner
from janus.parsers.reqs_parser import RequirementsParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class RequirementsDocumenter(Documenter):
    """RequirementsGenerator

    A class that translates code from one programming language to its requirements.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_prompt("requirements")
        self._combiner = ChunkCombiner()
        self._parser = RequirementsParser()

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
