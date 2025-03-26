import unittest

from janus.language.block import CodeBlock
from janus.parsers.eval_parsers.incose_parser import IncoseParser
from janus.parsers.eval_parsers.uml_parser import UMLParser


class TestUMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = UMLParser()
        self.test_codeblock = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text='{"diagrams":"@startuml test @enduml"}',
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )
        self.test_response = (
            '{"completeness": {"reasoning": "The diagram addresses most '
            "of the essential functionality of the provided source code. It covers "
            "the import"
            " statements, function definition, major steps within the function, and "
            "how the "
            'function interacts with other parts of the code.", "score": 3}, '
            '"hallucination":'
            ' {"reasoning": "The diagram provides true information based on the provided '
            "source code. Each step and note corresponds accurately to the code's "
            'operations and imports.", "score": 4}, "readability": {"reasoning": '
            '"The diagram'
            " is generally clear, with well-separated sections and notes that "
            "explain each "
            "step. However, the amount of detail in some notes might be overwhelming "
            "for "
            'quick understanding.", "score": 3}, "usefulness": {"reasoning": '
            '"The diagram '
            "is useful for an average programmer to understand the flow of the "
            "'aggregate'"
            " function. It highlights important steps and the sequence of "
            "operations, which "
            'aids in comprehension.", "score": 3}'
        )

    def test_parse_input(self):
        self.assertEqual(
            self.parser.parse_input(self.test_codeblock),
            '{"diagrams": ["@startuml test @enduml"]}',
        )

    def test_parse(self):
        self.assertIsInstance(self.parser.parse(self.test_response), str)


class TestIncoseParser(unittest.TestCase):
    def setUp(self):
        self.parser = IncoseParser()
        self.test_input = (
            '{"requirements":'
            '[["## Software Requirements Specification", '
            '"### 1. Introduction", "This document outlines the software '
            'requirements", "### 2. Scope", "This document specifies the '
            "functional requirements of the `aggregate` function. It does not "
            "cover non-functional requirements or implementation specifics of "
            'the legacy programming language.", "### 3. Functional '
            'Requirements", "#### 3.1 Main Functionality", "**FR-1**: The '
            "system shall provide a function `aggregate` that aggregates and "
            'translates source code files.", "#### 3.2 Input Parameters", '
            '"**FR-2**: The function shall accept the following input '
            'parameters:", "- `input_dir` (Path): The directory containing", '
            ' "### 4. Non-Functional Requirements", "The'
            " function shall handle errors gracefully, providing meaningful "
            "error messages and storing relevant failure information as "
            'specified.", "### 5. Dependencies", "**DEP-1**: The '
            "function shall depend on the following modules and their "
            'equivalents in the modern programming language:", "- '
            '`pathlib.Path`", "- `typing.List`", "- '
            '`janus.converter.aggregator.Aggregator`"]]}'
        )
        self.test_codeblock = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text=self.test_input,
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[],
            previous_generations=[{"input": "test"}],
        )

    def test_parse_input(self):
        self.assertIsInstance(self.parser.parse_input(self.test_codeblock), str)
