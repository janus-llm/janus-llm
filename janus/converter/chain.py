from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.utils.logger import create_logger

log = create_logger(__name__)


class ConverterChain(Converter):
    """
    Class for representing multiple converters chained together
    """

    def __init__(self, *args, **kwargs) -> None:
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
            use_janus_inputs=self._converters[0]._use_janus_inputs,
            input_types=self._converters[0]._input_types,
            input_labels=self._converters[0]._input_labels,
            output_type=self._converters[-1]._output_type,
            output_label=self._converters[-1]._output_label,
        )
        super().__init__(**kwargs)

    def translate_blocks(
        self, input_blocks: CodeBlock | list[CodeBlock], failure_path: Path | None = None
    ):
        input_blocks = self._filter_blocks(input_blocks)

        def _failed(blocks):
            if isinstance(blocks, list):
                return any(_failed(b) for b in blocks)
            return not blocks.translated

        def _to_codeblock(blocks):
            if isinstance(blocks, list):
                return [_to_codeblock(b) for b in blocks]
            return blocks.to_codeblock()

        failed = False
        for i, converter in enumerate(self._converters):
            translated_code_blocks = converter.translate_blocks(input_blocks)
            if _failed(translated_code_blocks):
                log.info(
                    f"Error: chain failed to translate at step {i}:"
                    f"{self._converters[i].__class__.__name__}"
                )
                failed = True
                break
            input_blocks = _to_codeblock(translated_code_blocks)
        if not failed and _failed(translated_code_blocks):
            log.info(
                f"Error: chain failed to translate at step {len(self._converters)-1}: "
                f"{self._converters[-1].__class__.__name__}"
            )
        return translated_code_blocks

    def _get_output_obj(
        self, block: TranslatedCodeBlock | list, combine_children: bool = True
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        output_obj = super()._get_output_obj(block, combine_children)
        intermediate_outputs = []
        for i, intermediate_out in enumerate(block.previous_generations):
            if isinstance(intermediate_out, TranslatedCodeBlock):
                intermediate_outputs.append(
                    self._converters[i]._get_output_obj(intermediate_out)
                )
            else:
                intermediate_outputs.append(intermediate_out)
        intermediate_outputs.append(self._converters[-1]._get_output_obj(block))
        output_obj["intermediate_outputs"] = intermediate_outputs
        metadata = output_obj["metadata"]
        metadata["cost"] += sum(
            b.cost if isinstance(b, TranslatedCodeBlock) else b["metadata"]["cost"]
            for b in block.previous_generations
        )
        metadata["processing_time"] += sum(
            b.processing_time
            if isinstance(b, TranslatedCodeBlock)
            else b["metadata"]["processing_time"]
            for b in block.previous_generations
        )
        metadata["num_requests"] += sum(
            b.total_num_requests
            if isinstance(b, TranslatedCodeBlock)
            else b["metadata"]["num_requests"]
            for b in block.previous_generations
        )
        metadata["input_tokens"] += sum(
            b.total_request_input_tokens
            if isinstance(b, TranslatedCodeBlock)
            else b["metadata"]["input_tokens"]
            for b in block.previous_generations
        )
        metadata["output_tokens"] += sum(
            b.total_request_output_tokens
            if isinstance(b, TranslatedCodeBlock)
            else b["metadata"]["output_tokens"]
            for b in block.previous_generations
        )
        output_obj["metadata"] = metadata
        if len(block.previous_generations) > 0:
            b = block.previous_generations[0]
            output_obj["input"] = (
                (b.original.text or "")
                if isinstance(b, TranslatedCodeBlock)
                else b["input"]
            )
        return output_obj
