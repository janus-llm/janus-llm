from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock


class ConverterPassthrough(Converter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def _translate_block(self, block: CodeBlock) -> TranslatedCodeBlock | CodeBlock:
        return block
