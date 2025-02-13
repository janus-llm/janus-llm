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

    def _combine_metadata(self, metadatas: list[dict]):
        metadata = super()._combine_metadata(metadatas)
        if isinstance(metadata["type"], list):
            metadata["type"] = metadata["type"][-1]
        if isinstance(metadata["label"], list):
            metadata["label"] = metadata["label"][-1]
        metadata["type"] = metadatas[-1]["type"]
        metadata["label"] = metadatas[-1]["label"]
        return metadata

    def _get_output_obj(
        self,
        block: TranslatedCodeBlock | BlockCollection,
        combine_children: bool = True,
        include_previous_outputs: bool = True,
    ) -> dict[str, int | float | str | dict[str, str] | dict[str, float]]:
        intermediate_outputs = []
        c_index = 0  # current converter index
        start_index = 0  # start index of newly generated intermediate outputs
        for g in block.previous_generations:
            if isinstance(g, dict):
                intermediate_outputs.append(g)
                # Find the first index where we generated code
                start_index += 1
            else:
                intermediate_outputs.append(
                    self._converters[c_index]._get_output_obj(
                        g, self._converters[c_index]._combine_output, False
                    )
                )
                c_index += 1
        intermediate_outputs.append(
            self._converters[-1]._get_output_obj(
                block, self._converters[-1]._combine_output, False
            )
        )
        out = dict(
            input=intermediate_outputs[start_index]["input"],
            metadata=self._combine_metadata(
                [i["metadata"] for i in intermediate_outputs]
            ),
            outputs=intermediate_outputs[-1]["outputs"],
        )
        if include_previous_outputs:
            out["intermediate_outputs"] = intermediate_outputs
        return out
