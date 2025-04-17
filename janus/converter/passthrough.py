from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock


class ConverterPassthrough(Converter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def translate_block(
        self, input_block: CodeBlock, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        self._output_label = input_block.block_label
        self._output_type = input_block.block_type
        res = super().translate_block(input_block, failure_path)

        last_gen = input_block.previous_generations[-1]
        last_gen_block = TranslatedCodeBlock.from_janus_object(last_gen)
        res.original = last_gen_block.to_codeblock()
        res.previous_generations = input_block.previous_generations[:-1]
        return res

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        block.text = block.original.text
        block.tokens = block.original.tokens
        block.translated = True
