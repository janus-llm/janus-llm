import unittest
from unittest.mock import call, patch

from janus.converter.evaluate import (
    InlineCommentEvaluator,
    RequirementEvaluator,
    SummaryEvaluator,
    UMLEvaluator,
)
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.refiners.refiner import FixParserExceptions


class TestUMLEvaluator(unittest.TestCase):
    """Tests for the UMLEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = UMLEvaluator(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block(self, mock_translate_block, mock_split_text):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="This is UML",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

        translated_block = TranslatedCodeBlock(source, source.language, self.evaluator)
        mock_translate_block.return_value = translated_block

        actual = self.evaluator.translate_block(source)
        obj_str = '{"diagrams": "This is UML", "code": "test"}'
        mock_split_text.assert_called_with(obj_str, source.name)

        self.assertEqual(actual.original, source)
        self.assertEqual(actual.previous_generations, source.previous_generations)


class TestRequirementEvaluator(unittest.TestCase):
    """Tests for the RequirementEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.req_evaluator = RequirementEvaluator(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.req_evaluator._model_name, "gpt-4o")
        self.assertEqual(self.req_evaluator._source_language, "json")
        self.assertEqual(self.req_evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block(self, mock_translate_block, mock_split_text):
        """Test translate_block method"""

        self.req_evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='[["The program shall return 0"]]',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

        translated_block = TranslatedCodeBlock(
            source, source.language, self.req_evaluator
        )
        mock_translate_block.return_value = translated_block

        actual = self.req_evaluator.translate_block(source)
        obj_str = '{"requirements": ["The program shall return 0"], "code": "test"}'
        mock_split_text.assert_called_with(obj_str, source.name)

        self.assertEqual(actual.original, source)
        self.assertEqual(actual.previous_generations, source.previous_generations)

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block_with_eval_items_per_request(
        self, mock_translate_block, mock_split_text
    ):
        """Test translate_block method with eval_items_per_request set"""

        self.req_evaluator._use_janus_inputs = False
        self.req_evaluator.eval_items_per_request = 1

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='[["The program shall return 0", "The program will not crash"]]',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

        translated_block = TranslatedCodeBlock(
            source, source.language, self.req_evaluator
        )
        translated_block.text = '{"a":"b"}'
        translated_block2 = TranslatedCodeBlock(
            source, source.language, self.req_evaluator
        )
        translated_block2.text = '{"b":"c"}'

        mock_translate_block.side_effect = [translated_block, translated_block2]

        actual = self.req_evaluator.translate_block(source)

        mock_split_text.assert_has_calls(
            [
                call(
                    '{"requirements": ["The program shall return 0"], "code": "test"}',
                    source.name,
                ),
                call(
                    '{"requirements": ["The program will not crash"], "code": "test"}',
                    source.name,
                ),
            ]
        )

        self.assertEqual(actual.text, '{"a": "b", "b": "c"}')


class TestSummaryEvaluator(unittest.TestCase):
    """Tests for the SummaryEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = SummaryEvaluator(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block(self, mock_translate_block, mock_split_text):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="This is a summary",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

        translated_block = TranslatedCodeBlock(source, source.language, self.evaluator)
        mock_translate_block.return_value = translated_block

        actual = self.evaluator.translate_block(source)
        obj_str = '{"summary": "This is a summary", "code": "test"}'
        mock_split_text.assert_called_with(obj_str, source.name)

        self.assertEqual(actual.original, source)
        self.assertEqual(actual.previous_generations, source.previous_generations)


class TestInlineCommentEvaluator(unittest.TestCase):
    """Tests for the InlineCommentEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = InlineCommentEvaluator(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    def test_translate_block_with_no_comments(self):
        """Test translate_block method"""

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

        actual = self.evaluator.translate_block(source)

        self.assertEqual(actual, [])

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block(self, mock_translate_block, mock_split_text):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[
                {
                    "input": "*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>"  # noqa E501
                }
            ],
        )

        translated_block = TranslatedCodeBlock(source, source.language, self.evaluator)
        mock_translate_block.return_value = translated_block

        actual = self.evaluator.translate_block(source)
        obj_str = "*\n* <BLOCK_COMMENT 14b80530> first line\nDFHEISTG DSECT<INLINE_COMMENT dadfa102> second line"  # noqa E501
        mock_split_text.assert_called_with(obj_str, source.name)

        self.assertEqual(actual.original, source)
        self.assertEqual(actual.previous_generations, source.previous_generations)

    @patch("janus.converter.Converter._split_text")
    @patch("janus.converter.Converter.translate_block")
    def test_translate_block_with_eval_items_per_request(
        self, mock_translate_block, mock_split_text
    ):
        """Test translate_block method with eval_items_per_request set"""

        self.evaluator._use_janus_inputs = False
        self.evaluator.eval_items_per_request = 1

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[
                {
                    "input": "*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>"  # noqa E501
                }
            ],
        )

        translated_block = TranslatedCodeBlock(source, source.language, self.evaluator)
        translated_block.text = '{"a":"b"}'
        translated_block2 = TranslatedCodeBlock(source, source.language, self.evaluator)
        translated_block2.text = '{"b":"c"}'

        mock_translate_block.side_effect = [translated_block, translated_block2]

        actual = self.evaluator.translate_block(source)

        mock_split_text.assert_has_calls(
            [
                call(
                    "*\n* <BLOCK_COMMENT 14b80530> first line\nDFHEISTG DSECT",
                    source.name,
                ),
                call(
                    "*\n* \nDFHEISTG DSECT<INLINE_COMMENT dadfa102> second line",
                    source.name,
                ),
            ]
        )

        self.assertEqual(actual.text, '{"a": "b", "b": "c"}')
