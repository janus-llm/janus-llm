import json
import unittest
from unittest.mock import patch

from janus.converter.evaluate import (
    InlineCommentEvaluator,
    JavaCategoryEvaluator,
    RequirementEvaluator,
    SummaryEvaluator,
    UMLEvaluator,
)
from janus.language.block import CodeBlock, TranslatedCodeBlock, combine_metadata
from janus.refiners.refiner import FixParserExceptions


class TestUMLEvaluator(unittest.TestCase):
    """Tests for the UMLEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = UMLEvaluator(
            model="gpt-4o-mini",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o-mini")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="This is UML",
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        mock_run_chain.return_value = "This is evaluated UML"

        # Incorrect input type, should be skipped
        result = self.evaluator._translate_block(source)
        self.assertNotIsInstance(result, TranslatedCodeBlock)

        # Fix input type
        source.block_type = "diagram"
        result = self.evaluator._translate_block(source)

        obj_str = '{"eval_object": "This is UML", "code": "test"}'

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, "This is evaluated UML")
        self.assertEqual(result.original.text, obj_str)
        self.assertEqual(result.previous_generation, source.previous_generation)


class TestRequirementEvaluator(unittest.TestCase):
    """Tests for the RequirementEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = RequirementEvaluator(
            model="gpt-4o-mini",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o-mini")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='[["The program shall return 0"]]',
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        out_str = json.dumps(
            {
                "c3caa172": dict(
                    requirement="The program shall return 0", eval="Evaluations"
                )
            }
        )
        mock_run_chain.return_value = out_str

        # Incorrect input type, should be skipped
        result = self.evaluator._translate_block(source)
        self.assertNotIsInstance(result, TranslatedCodeBlock)

        # Fix input type
        source.block_type = "requirements"
        result = self.evaluator._translate_block(source)

        obj_str = '{"eval_object": ["The program shall return 0"], "code": "test"}'

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, out_str)
        self.assertEqual(result.original.text, obj_str)
        self.assertEqual(result.previous_generation, source.previous_generation)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block_with_eval_items_per_request(self, mock_run_chain):
        """Test translate_block method with eval_items_per_request set"""

        self.evaluator._use_janus_inputs = False
        self.evaluator._eval_items_per_request = 1
        self.evaluator._initialized = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='[["The program shall return 0", "The program will not crash"]]',
            block_type="requirements",
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        out_objs = [
            {"c3caa172": dict(requirement="The program shall return 0", eval="great")},
            {"fab48ab9": dict(requirement="The program will not crash", eval="terrible")},
        ]
        mock_run_chain.side_effect = [json.dumps(s) for s in out_objs]

        out_obj = {}
        for obj in out_objs:
            out_obj.update(obj)

        result = self.evaluator._translate_block(source)
        self.assertEqual(result.text, json.dumps(out_obj))


class TestSummaryEvaluator(unittest.TestCase):
    """Tests for the SummaryEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = SummaryEvaluator(
            model="gpt-4o-mini",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o-mini")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="This is a summary",
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        mock_run_chain.return_value = "Evaluated summary"

        # Incorrect input type, should be skipped
        result = self.evaluator._translate_block(source)
        self.assertNotIsInstance(result, TranslatedCodeBlock)

        # Fix input type
        source.block_type = "documentation"
        result = self.evaluator._translate_block(source)

        obj_str = '{"eval_object": "This is a summary", "code": "test"}'

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, "Evaluated summary")
        self.assertEqual(result.original.text, obj_str)
        self.assertEqual(result.previous_generation, source.previous_generation)


class TestInlineCommentEvaluator(unittest.TestCase):
    """Tests for the InlineCommentEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = InlineCommentEvaluator(
            model="gpt-4o-mini",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o-mini")
        self.assertEqual(self.evaluator._source_language, "json")
        self.assertEqual(self.evaluator._use_janus_inputs, True)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block_with_no_comments(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            block_type="cloze_comments",
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        # No comments in code, should skip
        result = self.evaluator._translate_block(source)
        self.assertIsNone(result.text)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            previous_generation={
                "input": "*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>",  # noqa E501
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()
        mock_run_chain.return_value = '{"14b80530": "great", "dadfa102": "terrible"}'

        # Incorrect input type, should be skipped
        result = self.evaluator._translate_block(source)
        self.assertNotIsInstance(result, TranslatedCodeBlock)

        # Fix input type
        source.block_type = "cloze_comments"

        result = self.evaluator._translate_block(source)

        obj_str = "*\n* <BLOCK_COMMENT 14b80530> first line\nDFHEISTG DSECT<INLINE_COMMENT dadfa102> second line"  # noqa E501

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, '{"14b80530": "great", "dadfa102": "terrible"}')
        self.assertEqual(result.original.text, obj_str)
        self.assertEqual(result.previous_generation, source.previous_generation)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block_with_eval_items_per_request(self, mock_run_chain):
        """Test translate_block method with eval_items_per_request set"""

        self.evaluator._use_janus_inputs = False
        self.evaluator._eval_items_per_request = 1

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"14b80530": "first line", "dadfa102": "second line"}',
            block_type="cloze_comments",
            previous_generation={
                "input": "*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>",  # noqa E501
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )
        source.mark_root()

        mock_run_chain.side_effect = ['{"14b80530": "great"}', '{"dadfa102": "terrible"}']

        result = self.evaluator._translate_block(source)
        result.previous_generation
        self.assertEqual(result.text, '{"14b80530": "great", "dadfa102": "terrible"}')


class TestJavaCategoryEvaluator(unittest.TestCase):
    """Tests for the JavaCategoryEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.evaluator = JavaCategoryEvaluator(
            model="gpt-4o-mini",
            source_language="java",
            refiner_types=[FixParserExceptions],
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.evaluator._model_name, "gpt-4o-mini")
        self.assertEqual(self.evaluator._source_language, "java")
        self.assertEqual(self.evaluator._use_janus_inputs, False)

    @patch("janus.converter.Converter._run_chain")
    def test_translate_block(self, mock_run_chain):
        """Test translate_block method"""

        self.evaluator._use_janus_inputs = False

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="java",
            text="public static void main string args etc.\nanother line\na third line",
        )
        source.mark_root()

        out_str = json.dumps(
            [
                {
                    "start_line": 1,
                    "end_line": 1,
                    "section_reasoning": "Looks like perfect code to me.",
                    "section_label": "clean_implementation",
                    "section_quality": 101,
                }
            ]
        )
        mock_run_chain.return_value = out_str

        result = self.evaluator._translate_block(source)

        obj_str = (
            "1    public static void main string args etc.\n"
            "2    another line\n"
            "3    a third line"
        )

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, out_str)
        self.assertEqual(result.original.text, obj_str)
        self.assertEqual(result.previous_generation, source.previous_generation)
