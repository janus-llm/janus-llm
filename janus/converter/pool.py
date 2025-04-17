from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import (
    BlockCollection,
    JanusOutputObject,
    TranslatedBlockCollection,
    TranslatedCodeBlock,
)


class ConverterPool(Converter):
    def __init__(self, converters: list[Converter], **kwargs):
        if len(converters) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in converters:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters: list[Converter] = converters
        if "source_language" in kwargs:
            for c in self._converters:
                c._set_source_language(kwargs["source_language"])
        if "model" in kwargs:
            for c in self._converters:
                c._model_name = kwargs["model"]
        super().__init__(**kwargs)

    def _combine_blocks(self, blocks: TranslatedBlockCollection) -> None:
        for b in blocks.blocks:
            if isinstance(b.converter, Converter):
                b.converter._combine_block(b)

    def translate_blocks(
        self, input_blocks: BlockCollection, failure_path: Path | None = None
    ):
        # TODO: Figure out how to handle partial failure (sp. writing to file)
        self._load_parameters()
        output_blocks: list[TranslatedCodeBlock] = []
        for c in self._converters:
            collection = c.translate_blocks(input_blocks)
            output_blocks += collection.blocks
        return TranslatedBlockCollection(output_blocks, input_blocks.previous_generations)

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | TranslatedBlockCollection | JanusOutputObject,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> JanusOutputObject:
        # If this is not a collection, no special processing needed
        #  (this should probably never happen, though)
        if isinstance(block, dict) or isinstance(block, TranslatedCodeBlock):
            return super()._get_output_obj(
                block=block,
                combine_children=combine_children,
                include_previous_outputs=include_previous_outputs,
            )

        janus_obj = block.to_janus_object(combine_children)
        if not include_previous_outputs:
            del janus_obj["intermediate_outputs"]

        # Make sure we use the converter-specific logic for constructing outputs
        janus_obj["outputs"] = [
            b.converter._get_output_obj(
                block=b,
                combine_children=b.converter._combine_output,
                include_previous_outputs=False,
            )
            if isinstance(b.converter, Converter)
            else b.to_janus_object()
            for b in block.blocks
        ]

        return janus_obj
