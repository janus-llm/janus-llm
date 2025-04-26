from janus.converter.converter import Converter
from janus.language.block import (
    CodeBlock,
    JanusOutputObject,
    TranslatedCodeBlock,
    combine_janus_objects,
)
from janus.utils.logger import create_logger

log = create_logger(__name__)


class IncompletePoolException(Exception):
    """An exception raised when at least one Converter in a ConverterPool fails
    to complete a single translation
    """

    pass


class ConverterPool(Converter):
    def __init__(self, converters: list[Converter], **kwargs):
        if len(converters) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in converters:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters: list[Converter] = converters
        if "model" in kwargs:
            for c in self._converters:
                c._model_name = kwargs["model"]
        super().__init__(**kwargs)

    def _combine_block(self, block: TranslatedCodeBlock) -> None:
        # For ConverterPool, each translated block has a child for each converter
        for child in block.children:
            if not isinstance(child, TranslatedCodeBlock):
                continue

            if not isinstance(child.converter, Converter):
                continue

            child.converter._combine_block(child)

    def _translate_blocks(self, blocks: list[CodeBlock]) -> list[TranslatedCodeBlock]:
        """For a ConverterChain, the output of _translate_blocks is not parallel to the
        input blocks, but instead to the member list of Converters. Each element
        in the returned list will be a TranslatedCodeBlock with *children*
        parallel to the input block list. If a converter did not translate a block
        (returning an untranslated CodeBlock), that block is dropped.
        """
        # Get a list of translations parallel to converters, with each element
        #  a list of translations corresponding to each block
        converter_translations: list[list[CodeBlock | TranslatedCodeBlock]] = [
            converter._translate_blocks(blocks) for converter in self._converters
        ]
        empty_converters = [
            converter.__class__.__name__
            for converter, trans in zip(self._converters, converter_translations)
            if not any(isinstance(b, TranslatedCodeBlock) for b in trans)
        ]
        if empty_converters:
            plural = len(empty_converters) > 1
            log.warning(
                f"{len(empty_converters)} Converter{'s' if plural else ''} failed to"
                f" generate any output ({', '.join(empty_converters)})"
            )

        # Nest each list of converter translations as children of a TranslatedCodeBlock
        translated_blocks = []
        for converter, trans in zip(self._converters, converter_translations):
            trans = [b for b in trans if isinstance(b, TranslatedCodeBlock)]
            if not trans:
                translated_blocks.extend(blocks)
                block = CodeBlock.get_empty()
                block.children = blocks
                translated_blocks.append(block)
                continue

            translated_block = TranslatedCodeBlock(
                original=None,
                language=converter._target_language,
                converter=converter,
                model_name=converter._model_name,
                block_type=converter._output_type,
                block_label=converter._output_label,
            )
            translated_block.children = trans

            # This block should be considered "translated" if *any* of of the
            #  converters successfully translated it.
            # TODO: This may conflict with TranslatedCodeBlock.translation_completed
            translated_block.translated = any(b.translated for b in trans)

            translated_blocks.append(translated_block)

        return translated_blocks

    def _get_output_obj(
        self,
        translation: list[TranslatedCodeBlock | CodeBlock] | JanusOutputObject,
    ) -> JanusOutputObject:
        translation = [t for t in translation if isinstance(t, TranslatedCodeBlock)]
        janus_object = super()._get_output_obj(translation)
        janus_object["metadata"]["converter_name"] = self.__class__.__name__
        janus_object["metadata"]["type"] = self._output_type
        janus_object["metadata"]["label"] = self._output_label
        janus_object["metadata"]["language"] = self._target_language

        for child in janus_object["outputs"]:
            child["metadata"]["translation_complete"] = any(
                b["metadata"]["translation_complete"] for b in child["outputs"]
            )
        janus_object["metadata"]["translation_complete"] = any(
            child["metadata"]["translation_complete"] for child in janus_object["outputs"]
        )
        return janus_object

        # We need to convert a list of objects each with a child per converter,
        #  to a list of objects each corresponding to a converter, each with children
        #  corresponding to each block. Essentially, invert the top layer of the tree.
        converter_to_blocks: dict[str, list[TranslatedCodeBlock]] = {
            (
                block.converter
                if isinstance(block.converter, str)
                else block.converter.__class__.__name__
            ): block.children
            for block in translation
        }

        if not all(converter_to_blocks.values()):
            empty_converters = [k for k, v in converter_to_blocks.items() if not v]
            plural = len(empty_converters) > 1
            raise IncompletePoolException(
                f"{len(empty_converters)} Converter{'s' if plural else ''} failed to"
                f" generate any output ({', '.join(empty_converters)})"
            )

        janus_objects = []
        input_objects = []
        for converter in self._converters:
            converter_name = converter.__class__.__name__
            blocks = converter_to_blocks[converter_name]
            blocks = [b for b in blocks if isinstance(b, TranslatedCodeBlock)]
            obj = converter._get_output_obj(blocks)  # type: ignore
            obj["metadata"]["translation_complete"] = any(b.translated for b in blocks)
            janus_objects.append(obj)
            input_objects.append(obj["input"])

        janus_object = combine_janus_objects(janus_objects)
        janus_object["metadata"]["converter_name"] = "ConverterPool"
        janus_object["metadata"]["language"] = self._target_language
        janus_object["metadata"]["type"] = self._output_type
        janus_object["metadata"]["label"] = self._output_label

        return janus_object

    def _translate_blocks_(
        self, blocks: list[CodeBlock]
    ) -> list[TranslatedCodeBlock | CodeBlock]:
        # Get a list of translations parallel to converters, with each element
        #  a list of translations corresponding to each block
        converter_translations: list[list[CodeBlock | TranslatedCodeBlock]] = [
            converter._translate_blocks(blocks) for converter in self._converters
        ]
        empty_converters = [
            converter.__class__.__name__
            for converter, trans in zip(self._converters, converter_translations)
            if not any(isinstance(b, TranslatedCodeBlock) for b in trans)
        ]
        if empty_converters:
            plural = len(empty_converters) > 1
            log.warning(
                f"{len(empty_converters)} Converter{'s' if plural else ''} failed to"
                f" generate any output ({', '.join(empty_converters)})"
            )

        # Transpose to list of translations parallel to blocks, with each element
        #  a list of translations corresponding to each Converter
        block_translations = zip(*converter_translations)

        # Nest each list of converter translations as children of a TranslatedCodeBlock
        translated_blocks = []
        for block, trans in zip(blocks, block_translations):
            trans = [b for b in trans if isinstance(b, TranslatedCodeBlock)]

            # If none of the converters converted the block, pass through original block
            if not trans:
                translated_blocks.append(block)
                continue

            translated_block = TranslatedCodeBlock(
                original=block,
                language=self._target_language,
                converter=self,
                model_name=self._model_name,
                block_type=self._output_type,
                block_label=self._output_label,
            )
            translated_block.children = trans

            # This block should be considered "translated" if *any* of of the
            #  converters successfully translated it.
            # TODO: This may conflict with TranslatedCodeBlock.translation_completed
            translated_block.translated = any(b.translated for b in trans)

            translated_blocks.append(translated_block)

        return translated_blocks

    def _get_output_obj_(
        self,
        translation: list[TranslatedCodeBlock | CodeBlock] | JanusOutputObject,
    ) -> JanusOutputObject:
        # If this is not a pool of outputs, no special processing needed
        #  (this should probably never happen, though)
        if not isinstance(translation, list):
            return super()._get_output_obj(translation)

        # We need to convert a list of objects each with a child per converter,
        #  to a list of objects each corresponding to a converter, each with children
        #  corresponding to each block. Essentially, invert the top layer of the tree.
        converter_to_blocks: dict[str, list[TranslatedCodeBlock]] = {
            converter.__class__.__name__: [] for converter in self._converters
        }
        for block in translation:
            if not isinstance(block, TranslatedCodeBlock):
                continue

            for child in block.children:
                converter = child.converter
                if not isinstance(converter, str):
                    converter = converter.__class__.__name__
                converter_to_blocks[converter].append(child)

        if not all(converter_to_blocks.values()):
            empty_converters = [k for k, v in converter_to_blocks.items() if not v]
            plural = len(empty_converters) > 1
            raise IncompletePoolException(
                f"{len(empty_converters)} Converter{'s' if plural else ''} failed to"
                f" generate any output ({', '.join(empty_converters)})"
            )

        janus_objects = []
        input_objects = []
        for converter in self._converters:
            converter_name = converter.__class__.__name__
            blocks = converter_to_blocks[converter_name]
            blocks = [b for b in blocks if isinstance(b, TranslatedCodeBlock)]
            obj = converter._get_output_obj(blocks)  # type: ignore
            obj["metadata"]["translation_complete"] = any(b.translated for b in blocks)
            janus_objects.append(obj)
            input_objects.append(obj["input"])

        janus_object = combine_janus_objects(janus_objects)
        janus_object["metadata"]["converter_name"] = "ConverterPool"
        janus_object["metadata"]["language"] = self._target_language
        janus_object["metadata"]["type"] = self._output_type
        janus_object["metadata"]["label"] = self._output_label

        return janus_object
