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

    def _run_converters(
        self, translated_code_block, name: str, failure_path: Path | None = None
    ):
        def _failed(block):
            if isinstance(block, list):
                return any(_failed(b) for b in block)
            return not block.translated

        failed = False
        for i, converter in enumerate(self._converters[1:]):
            if _failed(translated_code_block):
                log.info(
                    f"Error: chain failed to translate at step {i}:"
                    f"{self._converters[i].__class__.__name__}"
                )
                failed = True
                break
            if converter._use_janus_inputs:
                janus_obj = self._converters[i]._get_output_obj(translated_code_block)
                translated_code_block = converter.translate_janus_obj(
                    janus_obj, name, failure_path
                )
            else:
                translated_code_block = converter.translate_blocks(
                    translated_code_block.to_codeblock(), name, failure_path
                )
        if not failed and _failed(translated_code_block):
            log.info(
                f"Error: chain failed to translate at step {len(self._converters)-1}: "
                f"{self._converters[-1].__class__.__name__}"
            )

        return translated_code_block

    def translate_file(
        self, file: Path, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        """Translate a file using the chain of converters

        Arguments:
            file: The file to translate
            failure_path: The path to write the failure file to

        Returns:
            The translated code block
        """
        filename = file.name
        translated_code_block = self._converters[0].translate_file(file, failure_path)
        translated_code_block = self._run_converters(
            translated_code_block, filename, failure_path
        )
        return translated_code_block

    def translate_text(
        self, text: str, name: str, failure_path: Path | None = None
    ) -> TranslatedCodeBlock:
        """Translate a text using the chain of converters

        Arguments:
            text: The text to translate
            name: The name of the file
            failure_path: The path to write the failure file to

        Returns:
            The translated code block
        """
        translated_code_block = self._converters[0].translate_text(
            text, name, failure_path
        )
        translated_code_block = self._run_converters(
            translated_code_block, name, failure_path
        )
        return translated_code_block

    def translate_block(
        self,
        input_block: CodeBlock | list[CodeBlock],
        name: str,
        failure_path: Path | None = None,
    ) -> TranslatedCodeBlock:
        """Translate a block of code using the chain of converters

        Arguments:
            input_block: The block of code to translate
            name: The name of the file
            failure_path: The path to write the failure file to

        Returns:
            The translated code block
        """
        translated_code_block = self._converters[0].translate_blocks(
            input_block, name, failure_path
        )
        translated_code_block = self._run_converters(
            translated_code_block, name, failure_path
        )
        return translated_code_block

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
