from janus.converter.converter import Converter, IncompleteTranslationException
from janus.language.block import (
    CodeBlock,
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

        for i, converter in enumerate(self._converters):
            log.info(
                f"[bold green]Running Stage {i+1:d}: {converter.__class__.__name__}",
                extra={"markup": True},
            )
            translated_blocks = converter._translate_blocks(blocks)

            for block in translated_blocks:
                if isinstance(block, TranslatedCodeBlock):
                    # If the input block was labeled, maintain it in the working list
                    if block.original.block_label is not None:
                        translated_blocks.append(block.original)

            blocks = []
            for translated_block in translated_blocks:
                # If the converter ignored the block, maintain it in the working list
                if not isinstance(translated_block, TranslatedCodeBlock):
                    blocks.append(translated_block)
                    continue

                if not translated_block.translation_completed:
                    msg = (
                        f"{converter.__class__.__name__} failed on"
                        f" block '{translated_block.name}'"
                    )
                    log.error(msg)
                    continue
                    raise IncompleteTranslationException(
                        BrokenChainException(msg), translated_block
                    )

                # If the block was translated, convert the translation to an input
                block = translated_block.to_codeblock()
                block.mark_root()
                blocks.append(block)

        # Filter the blocks that were maintained only as source
        translated_blocks = [
            block for block in translated_blocks if block.block_label != "SOURCE"
        ]
        return translated_blocks

    def _get_output_obj(
        self,
        translation: list[TranslatedCodeBlock | CodeBlock] | JanusOutputObject,
    ) -> JanusOutputObject:
        if isinstance(translation, list):
            janus_object = super()._get_output_obj(translation)
        else:
            janus_object = translation

        # For each object, recurse through its inputs to get all the metadata
        #  to aggregate, and identify the original input
        original_inputs: set[str] = set()
        metadatas = []
        for obj in janus_object["outputs"]:
            while not isinstance(input := obj["input"], str):
                metadatas.append(obj["metadata"])

                # ConverterChain aggregates metadata and inputs
                if "converter_name" in obj["metadata"]:
                    if obj["metadata"]["converter_name"] == "ConverterChain":
                        break

                obj = input

            # Log the original input for this block
            original_inputs.add(input)

            # If input was chunked, must aggregate metadata
            if obj["outputs"]:
                original_metadata = combine_metadata(
                    chunk["metadata"] for chunk in obj["outputs"]
                )
            else:
                original_metadata = obj["metadata"]

        # If all the original inputs are the same, use that as the input to the chain
        if len(original_inputs) == 1:
            [janus_object["input"]] = original_inputs
        else:
            janus_object["input"] = "MULTIPLE"
            original_metadata = {}

        # Aggregate metadata, but use the original input metadata for start/end points
        metadata = combine_metadata(metadatas)
        input_keys = [
            "start_line",
            "start_char",
            "start_byte",
            "end_line",
            "end_char",
            "end_byte",
        ]
        for k in input_keys:
            if k in original_metadata:
                metadata[k] = original_metadata[k]

        # Input tokens to the chain are the output tokens of the original input
        if "output_tokens" in original_metadata:
            metadata["input_tokens"] = original_metadata["output_tokens"]
        elif "input_tokens" in original_metadata:
            metadata["input_tokens"] = original_metadata["input_tokens"]

        # Aggregate output tokens of final outputs
        metadata["output_tokens"] = sum(
            obj["metadata"]["output_tokens"] for obj in janus_object["outputs"]
        )

        # Chain output language is JSON
        metadata["language"] = "json"

        # Chain is complete if every step completed
        metadata["translation_complete"] = all(
            obj.get("translation_complete", True) for obj in janus_object["outputs"]
        )

        # Overwrite type and label if provided (otherwise, omit)
        metadata.pop("label", None)
        metadata.pop("type", None)
        if self._output_label is not None:
            metadata["label"] = self._output_label
        if self._output_type is not None:
            metadata["type"] = self._output_type

        janus_object["metadata"] = metadata

        return janus_object
