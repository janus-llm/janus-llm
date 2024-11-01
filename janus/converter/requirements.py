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

    @staticmethod
    def get_prompt_replacements(block) -> dict[str, str]:
        prompt_replacements: dict[str, str] = {"SOURCE_CODE": block.original.text}
        return prompt_replacements

    def _save_to_file(self, block: TranslatedCodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        output_list = list()
        # For each chunk of code, get generation metadata, the text of the code,
        # and the LLM generated requirements
        blocks = [block for block in block.children] if len(block.children) else [block]
        for block in blocks:
            code = block.original.text
            requirements = self._parser.parse_combined_output(block.complete_text)
            metadata = dict(
                retries=block.total_retries,
                cost=block.total_cost,
                processing_time=block.processing_time,
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
