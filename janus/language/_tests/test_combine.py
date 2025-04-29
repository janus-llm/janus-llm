import unittest

from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.language.combine import Combiner


class TestCombiner(unittest.TestCase):
    def setUp(self):
        self.combiner = Combiner()

        child_a = CodeBlock(
            id="child a",
            name="child a",
            node_type="child",
            language="plaintext",
            children=[],
            text="first child",
            affixes=("[prefix a]\n  ", "\n[suffix a]\n  "),
        )
        child_b = CodeBlock(
            id="child b",
            name="child b",
            node_type="child",
            language="plaintext",
            children=[],
            text="second child",
            affixes=("\n[prefix b]\n  ", "\n[suffix b]"),
        )
        self.block = CodeBlock(
            id="root",
            name="root",
            node_type="root",
            language="plaintext",
            children=[child_a, child_b],
            text=None,
            affixes=("[prefix]\n", "\n[suffix]"),
        )

        self.block.mark_root()

        self.translated_block = TranslatedCodeBlock(
            original=self.block,
            language="python",
            converter="Translator",
        )

    def test_combine(self):
        self.assertFalse(self.block.omit_prefix)
        self.assertFalse(self.block.children[0].omit_prefix)
        self.assertFalse(self.block.omit_suffix)
        self.assertFalse(self.block.children[-1].omit_suffix)

        prefix = "[prefix]\n[prefix a]\n  "
        central = "first child\n[suffix a]\n  second child"
        suffix = "\n[suffix b]\n[suffix]"

        # An untranslated TranslatedBlock is empty, so it will be all affixes
        self.assertEquals(
            f"{prefix}\n[suffix a]\n  {suffix}", self.translated_block.complete_text
        )

        # CodeBlock.complete_text should give the full string
        self.assertEquals(f"{prefix}{central}{suffix}", self.block.complete_text)

        # Before combining, self.block.text should be None
        self.assertEquals(None, self.block.text)

        self.combiner.combine(self.block)

        # After combining, self.block.text should be the contents of its children
        self.assertEquals(central, self.block.text)

        # CodeBlock.complete_text should not have been changed
        self.assertEquals(f"{prefix}{central}{suffix}", self.block.complete_text)


if __name__ == "__main__":
    unittest.main()
