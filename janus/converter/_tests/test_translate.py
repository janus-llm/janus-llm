import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Iterable, List, Optional, Type
from unittest.mock import patch

import pytest
from langchain.schema import Document
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VST, VectorStore

from janus.converter.diagram import DiagramGenerator
from janus.converter.requirements import RequirementsDocumenter
from janus.converter.translate import Translator
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.refiners.format import CodeFormatRefiner


class MockCollection(VectorStore):
    """Vector store for testing"""

    def __init__(self):
        self._add_texts_calls = 0

    def add_texts(
        self, texts: Iterable[str], metadatas: Optional[List[dict]] = None, **kwargs: Any
    ) -> List[str]:
        self._add_texts_calls += 1
        return ["id"]

    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        raise NotImplementedError("similarity_search() not implemented!")

    @classmethod
    def from_texts(
        cls: Type[VST],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> VST:
        raise NotImplementedError("from_texts() not implemented!")


class TestTranslator(unittest.TestCase):
    """Tests for the Translator class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator(
            model="gpt-4o-mini",
            source_language="fortran",
            target_language="python",
            target_version="3.10",
            splitter_type="ast-flex",
            refiner_types=[CodeFormatRefiner],
        )
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self.TEST_FILE_EMBEDDING_COUNT = 14

        self.req_translator = RequirementsDocumenter(
            model="gpt-4o-mini",
            source_language="fortran",
            prompt_templates="requirements",
        )

    @patch("janus.converter.Converter._run_chain")
    def test_translate(self, mock_run_chain):
        """Test translate method."""

        with open("janus/converter/_tests/fortran.json", "r") as f:
            expected = json.load(f)
            mock_run_chain.return_value = expected["output"].strip("\n")

        with tempfile.TemporaryDirectory(dir=self.test_file.parent) as tmpdirname:
            python_file = Path(tmpdirname) / f"{self.test_file.stem}.json"

            self.translator.translate(self.test_file.parent, tmpdirname)

            with open(python_file, "r") as f:
                actual = json.load(f)

            # TODO: Really shouldn't have to delete the input metadata here, not
            #       clear what the issue is, something to do with a newline getting
            #       added into the text at some point
            del expected["metadata"]
            del actual["metadata"]
            del expected["input"]["metadata"]
            del actual["input"]["metadata"]
            self.assertEqual(expected, actual)

    def test_invalid_selections(self) -> None:
        """Tests that settings values for the translator will raise exceptions"""
        self.assertRaises(
            ValueError, self.translator._set_target_language, "fake-lang", "1.0.0"
        )
        self.assertRaises(ValueError, self.translator._set_source_language, "fake-lang")
        self.assertRaises(ValueError, self.translator._set_splitter, "fake-splitter")
        self.assertRaises(
            ValueError, self.translator._set_refiner_types, ["fake-refiner"]
        )

        self.translator._prompt_template_names = ["fake-prompt"]
        self.assertRaises(ValueError, self.translator._load_parameters)

        self.translator._initialized = True
        try:
            self.translator._load_parameters()
        except Exception:
            self.fail("Initialization called after already being initialized")


class TestDiagramGenerator(unittest.TestCase):
    """Tests for the DiagramGenerator class."""

    def setUp(self):
        """Set up the tests."""
        self.diagram_generator = DiagramGenerator(
            model="gpt-4o-mini",
            source_language="fortran",
            diagram_type="Activity",
        )
        self.diagram_generator._load_parameters()

    def test_init(self):
        """Test __init__ method."""
        self.assertEqual(self.diagram_generator._model_name, "gpt-4o-mini")
        self.assertEqual(self.diagram_generator._source_language, "fortran")
        self.assertEqual(self.diagram_generator._diagram_type, "Activity")

    @patch("janus.converter.Converter._run_chain")
    def test_add_translation(self, mock_run_chain):
        """Test _add_translation method."""
        block = TranslatedCodeBlock(
            original=CodeBlock(
                id="test",
                name="Test Block",
                node_type="function",
                language="python",
                text="print('Hello, World!')",
                start_point=(0, 0),
                end_point=(1, 0),
                start_byte=0,
                end_byte=1,
                tokens=5,
                children=[],
            ),
            language="python",
            converter=self.diagram_generator,
        )
        mock_run_chain.return_value = "@startuml\n\nstart\n\n:Initialize Program;\n\n:Print 'Hello, World!';\n\n:End Program;\n\nstop\n\n@enduml"  # noqa E501
        self.diagram_generator._add_translation(block)
        self.assertTrue(block.translated)
        self.assertIsNotNone(block.text)
        self.assertIsNotNone(block.tokens)


@pytest.mark.parametrize(
    "source_language,prompt_template,expected_target_language,expected_target_version,",
    [
        ("python", "document_inline", "python", "3.10"),
        ("fortran", "document", "text", None),
        ("mumps", "requirements", "text", None),
        ("python", "simple", "javascript", "es6"),
    ],
)
def test_language_combinations(
    source_language: str,
    prompt_template: str,
    expected_target_language: str,
    expected_target_version: str,
):
    """Tests that translator target language settings are consistent
    with prompt template expectations.
    """
    translator = Translator(
        model="gpt-4o",
        source_language=source_language,
        target_language=expected_target_language,
        target_version=expected_target_version,
        prompt_templates=prompt_template,
    )
    translator._load_parameters()
    assert translator._target_language == expected_target_language  # nosec
    assert translator._target_version == expected_target_version  # nosec
    assert translator._splitter.language == source_language  # nosec
    assert translator._splitter.model.model_name == "gpt-4o"  # nosec
    assert translator._prompt_template_names == [prompt_template]  # nosec
