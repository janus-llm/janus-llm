from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.utils.logger import create_logger

log = create_logger(__name__)


class ConverterChain(Converter):
    """
    Class for representing multiple converters chained together
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in args:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters = args
        kwargs.update(
            source_language=self._converters[0].source_language,
            target_language=self._converters[-1]._target_language,
            target_version=self._converters[-1]._target_version,
            janus_inputs=self._converters[0]._janus_inputs,
        )
        super().__init__(**kwargs)

    def translate_file(
        self, file: Path, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        filename = file.name
        translated_code_block = self._converters[0].translate_file(file, failure_path)
        for i, converter in enumerate(self._converters[1:]):
            if converter._janus_inputs:
                janus_obj = self._converters[i]._get_output_obj(translated_code_block)
                translated_code_block = converter.translate_janus_obj(
                    janus_obj, filename, failure_path
                )
            else:
                translated_code_block = converter.translate_block(
                    translated_code_block.to_codeblock(), filename, failure_path
                )
        return translated_code_block

    def translate_text(self, text: str, name: str, failure_path: Path | None = None):
        translated_code_block = self._converters[0].translate_text(
            text, name, failure_path
        )
        for i, converter in enumerate(self._converters[1:]):
            if converter._janus_inputs:
                janus_obj = self._converters[i]._get_output_obj(translated_code_block)
                translated_code_block = converter.translate_janus_obj(
                    janus_obj, name, failure_path
                )
            else:
                translated_code_block = converter.translate_block(
                    translated_code_block.to_codeblock(), name, failure_path
                )
        return translated_code_block

    def translate_block(
        self,
        input_block: CodeBlock | list[CodeBlock],
        name: str,
        failure_path: Path | None = None,
    ):
        translated_code_block = self._converters[0].translate_block(
            input_block, name, failure_path
        )
        for i, converter in enumerate(self._converters[1:]):
            if converter._janus_inputs:
                janus_obj = self._converters[i]._get_output_obj(translated_code_block)
                translated_code_block = converter.translate_janus_obj(
                    janus_obj, name, failure_path
                )
            else:
                translated_code_block = converter.translate_block(
                    translated_code_block.to_codeblock(), name, failure_path
                )
        return translated_code_block
