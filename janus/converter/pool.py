from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import BlockCollection, CodeBlock, TranslatedCodeBlock


class ConverterPool(Converter):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in args:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters = args
        if "source_language" in kwargs:
            for c in self._converters:
                c.set_source_language(kwargs["source_language"])
        if "model" in kwargs:
            for c in self._converters:
                c.set_model(kwargs["model"])
        super().__init__(**kwargs)

    def translate_blocks(
        self, input_blocks: CodeBlock | BlockCollection, failure_path: Path | None = None
    ):
        output_blocks = []
        for c in self._converters:
            collection = c.translate_blocks(input_blocks)
            for b in collection.blocks:
                c._combiner.combine(b)
            output_blocks += collection.blocks
        return BlockCollection(output_blocks, input_blocks.previous_generations)

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | BlockCollection | dict,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        outputs = []
        for b in block.blocks:
            for c in self._converters:
                if c == b.converter:
                    outputs.append(c._get_output_obj(b, c._combine_output, False))
                    break

        def _get_input(block):
            if isinstance(block, BlockCollection):
                return self._combine_inputs([_get_input(b) for b in block.blocks])
            return block.original.text or ""

        out = dict(
            input=_get_input(block),
            metadata=dict(
                cost=block.total_cost,
                processing_time=block.total_processing_time,
                num_requests=block.total_num_requests,
                input_tokens=block.total_request_input_tokens,
                output_tokens=block.total_request_output_tokens,
                converter_name=self.__class__.__name__,
                type=block.block_type,
                label=block.block_label,
            ),
            outputs=outputs,
        )
        if include_previous_outputs and len(block.previous_generations) > 0:
            intermediate_outputs = [
                self._get_output_obj(g, combine_children, False)
                for g in block.previous_generations
                if isinstance(g, dict)
            ]
            if len(intermediate_outputs) > 0:
                out["intermediate_outputs"] = intermediate_outputs
        return out
