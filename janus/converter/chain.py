from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import (
    BlockCollection,
    JanusMetadata,
    JanusOutputObject,
    TranslatedBlockCollection,
    TranslatedCodeBlock,
    combine_metadata,
)
from janus.utils.logger import create_logger

log = create_logger(__name__)


class ConverterChain(Converter):
    """
    Class for representing multiple converters chained together
    """

    def __init__(self, converters: list[Converter], **kwargs) -> None:
        if len(converters) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in converters:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters: list[Converter] = converters
        head, tail = self._converters[0], self._converters[-1]
        kwargs.update(
            source_language=head.source_language,
            use_janus_inputs=head._use_janus_inputs,
            input_types=head._input_types,
            input_labels=head._input_labels,
            target_language=tail._target_language,
            target_version=tail._target_version,
            output_type=tail._output_type,
            output_label=tail._output_label,
        )
        super().__init__(**kwargs)

    def _combine_blocks(self, blocks: TranslatedBlockCollection):
        # TODO: Review (@wmacke)
        if not blocks.translation_completed:
            return

        # Match up converters with the previous generations they created
        for conv, block in zip(
            self._converters[-2::-1], blocks.previous_generations[::-1]
        ):
            conv._combine_blocks(block)
        self._converters[-1]._combine_blocks(blocks)

    def translate_blocks(
        self,
        block_collection: BlockCollection,
        failure_path: Path | None = None,
    ) -> TranslatedBlockCollection:
        for i, converter in enumerate(self._converters):
            translated_collection = converter.translate_blocks(block_collection)
            if not translated_collection.translation_completed:
                log.warning(
                    f"Error: chain failed to translate at step {i}: "
                    f"{converter.__class__.__name__}"
                )
                break
            block_collection = translated_collection.to_block_collection()
        return translated_collection

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | TranslatedBlockCollection | JanusOutputObject,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> JanusOutputObject:
        # Without intermediate outputs, nothing special for us to do
        if isinstance(block, dict) and "intermediate_outputs" not in block:
            return self._converters[-1]._get_output_obj(
                block=block,
                combine_children=self._converters[-1]._combine_output,
                include_previous_outputs=False,
            )

        # If translation was unsuccessful, don't bother with parsing
        if not isinstance(block, dict) and not block.translation_completed:
            return block.to_janus_object(combine_children)

        if isinstance(block, dict):
            intermediate_blocks = block["intermediate_outputs"]
        else:
            intermediate_blocks = block.previous_generations

        # Match converters up with their generations
        # Must be reversed before zipping in case of extra intermediate outputs
        #  from previous generations
        converter_generation_pairs = list(
            zip(self._converters[::-1], [block] + intermediate_blocks[::-1])
        )[::-1]
        intermediate_outputs = [
            conv._get_output_obj(
                block=prev_gen,
                combine_children=conv._combine_output,
                include_previous_outputs=False,
            )
            for conv, prev_gen in converter_generation_pairs
        ]
        metadata: JanusMetadata = combine_metadata(
            [obj["metadata"] for obj in intermediate_outputs]
        )
        metadata["type"] = intermediate_outputs[-1]["metadata"]["type"]
        metadata["label"] = intermediate_outputs[-1]["metadata"]["label"]
        out: JanusOutputObject = {
            "input": intermediate_outputs[0]["input"],
            "metadata": metadata,
            "outputs": intermediate_outputs[-1]["outputs"],
        }
        if include_previous_outputs:
            out["intermediate_outputs"] = intermediate_outputs

        return out
