from janus.converter.converter import Converter, IncompleteTranslationException
from janus.language.block import (
    CodeBlock,
    JanusMetadata,
    JanusOutputObject,
    TranslatedCodeBlock,
    combine_metadata,
)
from janus.utils.logger import create_logger

log = create_logger(__name__)


class BrokenChainException(Exception):
    """An exception raised when a ConverterChain fails in the middle of the translation"""

    pass


class ConverterChain(Converter):
    """
    Class for representing multiple converters chained together
    """

    def __init__(self, converters: list[Converter], **kwargs) -> None:
        if len(converters) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        self._converters: list[Converter] = converters
        super().__init__(**kwargs)
        # TODO: validate that input/output types/labels line up

    def _combine_blocks(self, blocks: list[TranslatedCodeBlock | CodeBlock]) -> None:
        for block in blocks:
            if isinstance(block, TranslatedCodeBlock):
                if isinstance(block.converter, Converter):
                    block.converter._combine_block(block)

    def _translate_blocks(
        self, blocks: list[CodeBlock]
    ) -> list[TranslatedCodeBlock | CodeBlock]:
        for block in blocks:
            if block.block_label is None:
                block.block_label = "SOURCE"

        for converter in self._converters:
            translated_blocks = converter._translate_blocks(blocks)

            for block in translated_blocks:
                if isinstance(block, TranslatedCodeBlock):
                    # If the input block was labeled, maintain it in the working list
                    if block.original.block_label is not None:
                        translated_blocks.append(block.original)

            blocks = []
            for b in translated_blocks:
                # If the converter ignored the block, maintain it in the working list
                if not isinstance(b, TranslatedCodeBlock):
                    blocks.append(b)
                    continue

                if not b.translation_completed:
                    msg = f"{converter.__class__.__name__} failed on block '{b.name}'"
                    raise IncompleteTranslationException(BrokenChainException(msg), b)

                # If the block was translated, convert the translation to an input
                blocks.append(b.to_codeblock())

        # Filter the blocks that were maintained only as source
        translated_blocks = [
            block for block in translated_blocks if block.block_label != "SOURCE"
        ]
        return translated_blocks

    def _get_output_obj(
        self,
        translation: list[TranslatedCodeBlock | CodeBlock] | JanusOutputObject,
    ) -> JanusOutputObject:
        metadatas = []
        curr_obj = super()._get_output_obj(translation)
        last_obj = curr_obj
        while True:
            metadatas.append(curr_obj["metadata"])
            if not isinstance(curr_obj["input"], dict):
                break
            curr_obj = curr_obj["input"]
        first_obj = curr_obj
        metadata = combine_metadata(metadatas)

        metadata: JanusMetadata = combine_metadata(metadatas)
        input_keys = [
            "input_tokens",
            "start_line",
            "start_char",
            "start_byte",
            "end_line",
            "end_char",
            "end_byte",
        ]
        output_keys = [
            "output_tokens",
            "language",
            "type",
            "label",
            "translation_complete",
        ]
        for k in input_keys:
            if k in first_obj["metadata"]:
                metadata[k] = first_obj["metadata"][k]
        for k in output_keys:
            if k in last_obj["metadata"]:
                metadata[k] = last_obj["metadata"][k]

        metadata["converter_name"] = "ConverterChain"
        janus_object: JanusOutputObject = {
            "input": first_obj["input"],
            "metadata": metadata,
            "outputs": last_obj["outputs"],
        }
        if "output" in last_obj:
            janus_object["output"] = last_obj["output"]

        return janus_object
