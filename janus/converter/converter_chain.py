from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.utils.logger import create_logger

log = create_logger(__name__)


class ConverterChain(Converter):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in args:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters = args
        kwargs.update(source_language=self._converters[0].source_language)
        super().__init__(**kwargs)
        self.set_target_language(
            self._converters[-1].target_language, self._converters[-1].target_version
        )

    def translate_file(
        self, file: Path, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        filename = file.name
        translated_code_block = self._converters[0].translate_file(file, failure_path)
        for converter in self._converters[1:]:
            translated_code_block = converter.translate_block(
                filename, translated_code_block.to_codeblock(), failure_path
            )
        return translated_code_block

    def translate_text(self, text: str, name: str, failure_path: Path | None = None):
        translated_code_block = self._converters[0].translate_text(
            text, name, failure_path
        )
        for converter in self._converters[1:]:
            translated_code_block = converter.translate_block(
                name, translated_code_block.to_codeblock(), failure_path
            )
        return translated_code_block

    def translate_block(
        self, name: str, input_block: CodeBlock, failure_path: Path | None = None
    ):
        translated_code_block = self._converters[0].translate_block(
            name, input_block, failure_path
        )
        for converter in self._converters[1:]:
            translated_code_block = converter.translate_block(
                name, translated_code_block.to_codeblock(), failure_path
            )
        return translated_code_block
