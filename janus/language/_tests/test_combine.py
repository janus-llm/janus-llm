import unittest

from janus.language.combine import CodeBlock, Combiner, TranslatedCodeBlock


class TestCombiner(unittest.TestCase):
    def setUp(self):
        self.combiner = Combiner()
        self.block = CodeBlock(
            id=1,
            name="test",
            node_type="test",
            language="python",
            text="# test",
            start_point=(0, 0),
            end_point=(0, 0),
            start_byte=0,
            end_byte=0,
            tokens=[],
            children=[
                CodeBlock(
                    id=2,
                    name="child",
                    node_type="test",
                    language="python",
                    text="test",
                    start_point=(0, 0),
                    end_point=(0, 0),
                    start_byte=0,
                    end_byte=0,
                    tokens=[],
                    children=[],
                )
            ],
        )
        self.translated_block = TranslatedCodeBlock(
            self.block,
            language="python",
        )

    def test_combine(self):
        self.combiner.combine(self.block)
        self.assertFalse(self.block.omit_prefix)

    def test_combine_children(self):
        self.block.complete = False
        self.combiner.combine_children(self.block)
        self.assertTrue(self.block.complete)

    def test_combine_children_with_translated_block(self):
        self.translated_block.complete = False
        self.combiner.combine_children(self.translated_block)
        self.assertFalse(self.translated_block.complete)

    def test_combine_children_with_text_none(self):
        self.combiner.combine_children(self.block)
        self.assertEqual(self.block.text, "# test")
        self.assertTrue(self.block.complete)


if __name__ == "__main__":
    unittest.main()
