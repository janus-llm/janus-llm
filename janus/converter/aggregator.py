from copy import deepcopy
from typing import List

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock


class Aggregator(Converter):
    def __init__(
        self,
        intermediate_converters: List[Converter],
        separator: str = "\n==============\n",
        **kwargs,
    ):
        """
        Initialization Method
        Arguments:
            intermediate_converters - list of converters to use
            separator: separator string to partition different outputs before combination
        """
        self._intermediate_converters = intermediate_converters
        self._separator = separator
        super().__init__(**kwargs)
        self._load_parameters()

    def _iterative_translate(self, root: CodeBlock) -> TranslatedCodeBlock:
        res = TranslatedCodeBlock(root, language=self._target_language)
        return self._recursive_translate(res)

    def _recursive_translate(self, root: TranslatedCodeBlock) -> None:
        """
        Recursively translates code blocks from a bottom up approach
        """
        original_text = root.original.text
        if len(root.children) > 0:
            for c in root.children:
                self._recursive_translate(c)
            root.original.text = self._combine_blocks(root.children, self._separator)
        else:
            int_reps = [deepcopy(root) for ic in self._intermediate_converters]
            for ic, r in zip(self._intermediate_converters, int_reps):
                ic._add_translation(r)
            root.original.text = self._combine_blocks(int_reps, self._separator)
        self._add_translation(root)
        root.original.text = original_text
        return root

    def _combine_blocks(self, blocks: List[TranslatedCodeBlock], separator: str) -> str:
        """
        Combines code blocks into a single piece of text
        """
        return separator.join([block.text for block in blocks])
