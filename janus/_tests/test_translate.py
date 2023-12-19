import unittest
from pathlib import Path
from typing import Any, Iterable, List, Optional, Type

import pytest
from langchain.schema import Document
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VST, VectorStore

from ..translate import Translator

# from langchain.vectorstores import Chroma


# from ..utils.enums import EmbeddingType


def print_query_results(query, n_results):
    # print(f"\n{query}")
    # count = 1
    # for t in n_results:
    #     short_code = (
    #         (t[0].page_content[0:50] + "..")
    #         if (len(t[0].page_content) > 50)
    #         else t[0].page_content
    #     )
    #     return_index = short_code.find("\n")
    #     if -1 != return_index:
    #         short_code = short_code[0:return_index] + ".."
    #     print(
    #         f"{count}. @ {t[0].metadata['start_line']}-{t[0].metadata['end_line']}"
    #         f" -- {t[1]} -- {short_code}"
    #     )
    #     count += 1
    pass


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


# class MockEmbeddingsFactory(EmbeddingsFactory):
#     """Embeddings for testing - uses MockCollection"""
#
#     def get_embeddings(self) -> Embeddings:
#         return MockCollection()
#


class TestTranslator(unittest.TestCase):
    """Tests for the Translator class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator(
            model="gpt-3.5-turbo",
            source_language="fortran",
            target_language="python",
            target_version="3.10",
        )
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self.TEST_FILE_EMBEDDING_COUNT = 14

        self.req_translator = Translator(
            model="gpt-3.5-turbo",
            # embeddings_override=MockEmbeddingsFactory(),
            source_language="fortran",
            target_language="text",
            target_version="3.10",
            prompt_template="requirements",
            parser_type="text",
        )

    @pytest.mark.translate
    def test_translate(self):
        """Test translate method."""
        # Delete a file if it's already there
        python_file = self.test_file.parent / "python" / f"{self.test_file.stem}.py"
        python_file.unlink(missing_ok=True)
        python_file.parent.rmdir() if python_file.parent.is_dir() else None
        self.translator.translate(self.test_file.parent, self.test_file.parent / "python")
        # Only check the top-most level functionality, since it should be handled by other
        # unit tests anyway
        self.assertTrue(python_file.exists())

        # def test_embeddings(self):
        #     """Testing access to embeddings"""
        #     vector_store = self.translator.embeddings(EmbeddingType.SOURCE)
        #     self.assertIsInstance(vector_store, Chroma, "Unexpected vector store type!")
        #     self.assertEqual(
        #         0, vector_store._collection.count(), "Non-empty initial vector store?"
        #     )
        #
        #     self.translator.set_model("llama")
        #     self.translator._load_parameters()
        #     vector_store = self.translator.embeddings(EmbeddingType.SOURCE)
        #     self.assertIsInstance(vector_store, Chroma)
        #     self.assertEqual(
        #         0, vector_store._collection.count(), "Non-empty initial vector store?"
        #     )

        # def test_embed_split_source(self):
        #     """Characterize _embed method"""
        #     mock_embeddings = MockEmbeddingsFactory()
        #     self.translator.set_embeddings(mock_embeddings)
        #     self.translator._load_parameters()
        #     input_block = self.translator.splitter.split(self.test_file)
        #     self.assertIsNone(
        #         input_block.text, "Root node of input text shouldn't contain text"
        #     )
        #     self.assertIsNone(input_block.embedding_id, "Precondition failed")
        #
        #     result = self.translator._embed(
        #         input_block, EmbeddingType.SOURCE, self.test_file.name
        #     )
        #
        #     self.assertFalse(result, "Nothing to embed, so should have no result")
        #     self.assertIsNone(
        # input_block.embedding_id, "Embeddings should not have changed")

        # def test_embed_has_values_for_each_non_empty_node(self):
        #     """Characterize our sample fortran file"""
        #     mock_embeddings = MockEmbeddingsFactory()
        #     self.translator.set_embeddings(mock_embeddings)
        #     self.translator._load_parameters()
        #     input_block = self.translator.splitter.split(self.test_file)
        #     self.translator._embed_nodes_recursively(
        #         input_block, EmbeddingType.SOURCE, self.test_file.name
        #     )
        #     has_text_count = 0
        #     has_embeddings_count = 0
        #     nodes = [input_block]
        #     while nodes:
        #         node = nodes.pop(0)
        #         if node.text:
        #             has_text_count += 1
        #         if node.embedding_id:
        #             has_embeddings_count += 1
        #         nodes.extend(node.children)
        #     self.assertEqual(
        #         self.TEST_FILE_EMBEDDING_COUNT,
        #         has_text_count,
        #         "Parsing of test_file has changed!",
        #     )
        #     self.assertEqual(
        #         self.TEST_FILE_EMBEDDING_COUNT,
        #         has_embeddings_count,
        #         "Not all non-empty nodes have embeddings!",
        #     )

        # def test_embed_nodes_recursively(self):
        #     mock_embeddings = MockEmbeddingsFactory()
        #     self.translator.set_embeddings(mock_embeddings)
        #     self.translator._load_parameters()
        #     input_block = self.translator.splitter.split(self.test_file)
        #     self.translator._embed_nodes_recursively(
        #         input_block, EmbeddingType.SOURCE, self.test_file.name
        #     )
        #     nodes = [input_block]
        #     while nodes:
        #         node = nodes.pop(0)
        #         self.assertEqual(node.text is not None, node.embedding_id is not None)
        #         nodes.extend(node.children)

        # @pytest.mark.slow
        # def test_translate_file_adds_source_embeddings(self):
        #     mock_embeddings = MockEmbeddingsFactory()
        #     self.translator.set_embeddings(mock_embeddings)
        #     self.translator._load_parameters()
        #     vector_store = self.translator.embeddings(EmbeddingType.SOURCE)
        #     self.assertEqual(0, vector_store._add_texts_calls, "precondition")
        #
        #     self.translator.translate_file(self.test_file)
        #
        #     self.assertEqual(
        #         self.TEST_FILE_EMBEDDING_COUNT,
        #         vector_store._add_texts_calls,
        #         "Did not find expected source embeddings",
        #     )

        # @pytest.mark.slow
        # def test_embeddings_usage(self):
        #     """Noodling on use of embeddings
        #     To see results have to uncomment print_query_results() above
        #     """
        #     input_block = self.translator.splitter.split(self.test_file)
        #     self.translator._embed_nodes_recursively(
        #         input_block, EmbeddingType.SOURCE, self.test_file.name
        #     )
        #     vector_store = self.translator.embeddings(EmbeddingType.SOURCE)
        #
        #     # this symbol has the lowest relevance scores of any in this test, but
        #     # still not very low; multiple embedded nodes contain it
        #     QUERY_STRING = "IWX_BAND_START"
        #     query = self.translator._embeddings._embeddings.embed_query(QUERY_STRING)
        #     n_results = vector_store.similarity_search_by_vector_with_relevance_scores(
        #         embedding=query,
        #         k=10,
        #         where_document={"$contains": QUERY_STRING},
        #     )
        #     self.assertTrue(len(n_results) > 1, "Why was valid symbol not found?")
        #     print_query_results(QUERY_STRING, n_results)

        # in the XYZZY test, the least dissimilar results were the start and finish lines
        # 0, and 415, which produced a similarity score of 0.47:

        # QUERY_STRING = "XYZZY"
        # query = self.translator._embeddings.embed_query(QUERY_STRING)
        # n_results = vector_store.similarity_search_by_vector_with_relevance_scores(
        #     embedding=query,
        #     k=10,
        #     # filter={"end_line": 15},
        #     # filter={"$and": [{"end_line": 15}, {"tokens": {"$gte": 21}}]},
        #     # where_document={"$contains": QUERY_STRING},
        # )
        # print_query_results(QUERY_STRING, n_results)
        # # self.assertTrue(len(n_results) == 0, "Invalid symbol was found?")

        # # only returns a single result because only 1 embedded node contains
        # #   CSV_ICASEARR:
        # QUERY_STRING = "What is the use of CSV_ICASEARR?"
        # query = self.translator._embeddings._embeddings.embed_query(QUERY_STRING)
        # n_results = vector_store.similarity_search_by_vector_with_relevance_scores(
        #     embedding=query,
        #     k=10,
        #     # where_document={"$contains": QUERY_STRING},
        #     where_document={"$contains": "CSV_ICASEARR"},
        # )
        # print_query_results(QUERY_STRING, n_results)
        # self.assertTrue(len(n_results) == 1, "Was splitting changed?")
        #
        # # trimmed out some characters from line 43, and still not very similar scoring
        # QUERY_STRING = "IYL_EDGEBUFFER EDGEBUFFER IGN_MASK CELLSIZE"
        # query = self.translator._embeddings._embeddings.embed_query(QUERY_STRING)
        # n_results = vector_store.similarity_search_by_vector_with_relevance_scores(
        #     embedding=query,
        #     k=10,
        #     # where_document={"$contains": QUERY_STRING},
        # )
        # print_query_results(QUERY_STRING, n_results)
        #
        # # random string (as bad as XYZZY), but searching for a specific line
        # QUERY_STRING = "ghost in the invisible moon"
        # query = self.translator._embeddings._embeddings.embed_query(QUERY_STRING)
        # n_results = vector_store.similarity_search_by_vector_with_relevance_scores(
        #     embedding=query,
        #     k=10,
        #     filter={"$and": [{"end_line": 90}, {"tokens": {"$gte": 21}}]},
        # )
        # print_query_results(QUERY_STRING, n_results)
        # self.assertTrue(len(n_results) == 1, "Was splitting changed?")

    def test_output_as_requirements(self):
        """Is output type requirements?"""
        self.assertFalse(self.translator.outputting_requirements())
        self.assertTrue(self.req_translator.outputting_requirements())

    # @pytest.mark.slow
    # def test_document_embeddings_added_by_translate(self):
    #     vector_store = self.req_translator.embeddings(EmbeddingType.REQUIREMENT)
    #     self.assertEqual(0, vector_store._add_texts_calls, "Precondition failed")
    #     self.req_translator.translate(self.test_file.parent, self.test_file.parent,
    #                                   True)
    #     self.assertTrue(vector_store._add_texts_calls > 0, "Why no documentation?")

    # @pytest.mark.slow
    # def test_embed_requirements(self):
    #     vector_store = self.req_translator.embeddings(EmbeddingType.REQUIREMENT)
    #     translated = self.req_translator.translate_file(self.test_file)
    #     self.assertEqual(
    #         0,
    #         vector_store._add_texts_calls,
    #         "Unexpected requirements added in translate_file",
    #     )
    #     result = self.req_translator._embed(
    #         translated, EmbeddingType.REQUIREMENT, self.test_file.name
    #     )
    #     self.assertFalse(result, "No text in root node, so should generate no docs")
    #     self.assertIsNotNone(translated.children[0].text, "Data changed?")
    #     result = self.req_translator._embed(
    #         translated.children[0], EmbeddingType.REQUIREMENT, self.test_file.name
    #     )
    #     self.assertTrue(result, "No docs generated for first child node?")

    def test_invalid_selections(self) -> None:
        """Tests that settings values for the translator will raise exceptions"""
        self.assertRaises(
            ValueError, self.translator.set_target_language, "gobbledy", "goobledy"
        )
        self.assertRaises(ValueError, self.translator.set_parser_type, "blah")
        self.assertRaises(
            ValueError, self.translator.set_source_language, "scribbledy-doop"
        )
        self.translator.set_prompt("pish posh")
        self.assertRaises(ValueError, self.translator._load_parameters)


@pytest.mark.parametrize(
    "source_language,prompt_template,expected_target_language,expected_target_version,"
    "parser_type",
    [
        ("python", "document_inline", "python", "3.10", "code"),
        ("fortran", "document", "text", None, "text"),
        ("mumps", "requirements", "text", None, "text"),
        ("python", "simple", "javascript", "es6", "code"),
    ],
)
def test_language_combinations(
    source_language: str,
    prompt_template: str,
    expected_target_language: str,
    expected_target_version: str,
    parser_type: str,
):
    """Tests that translator target language settings are consistent
    with prompt template expectations.
    """
    translator = Translator(model="gpt-3.5-turbo")
    translator.set_model("gpt-3.5-turbo-16k")
    translator.set_source_language(source_language)
    translator.set_target_language(expected_target_language, expected_target_version)
    translator.set_parser_type(parser_type)
    translator.set_prompt(prompt_template)
    translator._load_parameters()
    assert translator._target_language == expected_target_language  # nosec
    assert translator._target_version == expected_target_version  # nosec
    assert translator._parser_type == parser_type  # nosec
    assert translator._splitter.language == source_language  # nosec
    assert translator._splitter.model.model_name == "gpt-3.5-turbo-16k"  # nosec
    assert translator._prompt_engine._template_name == prompt_template  # nosec
