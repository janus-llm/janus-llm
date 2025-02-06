from pathlib import Path

from janus.converter.converter import Converter
from janus.language.block import BlockCollection, CodeBlock, TranslatedCodeBlock
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
        failed = False
        for i, converter in enumerate(self._converters):
            translated_code_blocks = converter.translate_blocks(input_blocks)
            if not translated_code_blocks.translation_completed:
                log.info(
                    f"Error: chain failed to translate at step {i}:"
                    f"{self._converters[i].__class__.__name__}"
                )
                failed = True
                break
            input_blocks = translated_code_blocks.to_codeblock()
        if not failed and not translated_code_blocks.translation_completed:
            log.info(
                f"Error: chain failed to translate at step {len(self._converters)-1}: "
                f"{self._converters[-1].__class__.__name__}"
            )
        return translated_code_blocks

    def _get_output_obj(
        self, block: TranslatedCodeBlock | BlockCollection, combine_children: bool = True
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        intermediate_outputs = []
        c_index = 0
        for g in block.previous_generations:
            if isinstance(g, dict):
                intermediate_outputs.append(g)
            else:
                intermediate_outputs.append(
                    self._converters[c_index]._get_output_obj(
                        g, self._converters[c_index]._combine_output
                    )
                )
                c_index += 1
        assert c_index == len(self._converters) - 1
        intermediate_outputs.append(
            self._converters[-1]._get_output_obj(
                block, self._converters[-1]._combine_output
            )
        )
        return dict(
            input=intermediate_outputs[0]["input"],
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
            outputs=intermediate_outputs[-1],
            intermediate_outputs=intermediate_outputs,
        )
