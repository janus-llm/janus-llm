import unittest

from janus.converter.evaluate import RequirementEvaluator, UMLEvaluator
from janus.language.block import CodeBlock, combine_metadata
from janus.refiners.refiner import FixParserExceptions


class TestUMLEvaluator(unittest.TestCase):
    """Tests for the UMLEvaluator class"""

    def setUp(self):
        """Set up the tests"""
        self.uml_evaluator = UMLEvaluator(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.uml_evaluator._model_name, "gpt-4o")
        self.assertEqual(self.uml_evaluator._source_language, "json")
        self.assertEqual(self.uml_evaluator._use_janus_inputs, True)

    def test_partial_translate_block(self):
        """Test part of the translate_block method in the
        UMLEvaluator. We aren't testing the full method, since that requires
        sending an LLM request."""

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )

        self.assertEqual(self.uml_evaluator._translate_block(source), source)


class TestRequirementEvaluator(unittest.TestCase):
    """Tests for the UMLEvaluator class"""

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

    def test_partial_translate_block(self):
        """Test part of the translate_block method in the
        RequirementsEvaluator. We aren't testing the full method, since that requires
        sending an LLM request."""

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="{}",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generation={
                "input": "test",
                "metadata": combine_metadata([]),
                "outputs": [],
            },
        )

        self.assertEqual(self.req_evaluator._translate_block(source), source)
