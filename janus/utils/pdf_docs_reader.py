import os
import time
from pathlib import Path
from typing import List, Optional

import joblib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from janus.utils.logger import create_logger

log = create_logger(__name__)


class PDFDocsReader:
    def __init__(
        self,
        language: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None,
        vectorizer: CountVectorizer = TfidfVectorizer(),
    ):
        self.retrieval_docs_dir: Path = Path(
            os.getenv("RETRIEVAL_DOCS_DIR", "retrieval_docs")
        )
        self.language = language
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.start_page = start_page
        self.end_page = end_page
        self.vectorizer = vectorizer
        self.documents = self.load_and_chunk_pdf()
        self.doc_vectors = self.vectorize_documents()

    def load_and_chunk_pdf(self) -> List[str]:
        pdf_path = self.retrieval_docs_dir / f"{self.language}.pdf"
        pickled_documents_path = (
            self.retrieval_docs_dir / f"{self.language}_documents.pkl"
        )

        if pickled_documents_path.exists():
            log.debug(
                f"Loading pre-chunked PDF from {pickled_documents_path}. "
                f"If you want to regenerate retrieval docs for {self.language}, "
                f"delete the file at {pickled_documents_path}, "
                f"then add a new {self.language}.pdf."
            )
            documents = joblib.load(pickled_documents_path)
        else:
            if not pdf_path.exists():
                raise FileNotFoundError(
                    f"Language docs retrieval is enabled, but no PDF for language "
                    f"'{self.language}' was found. Move a "
                    f"{self.language} reference manual to "
                    f"{pdf_path.absolute()} "
                    f"(the path to the directory of PDF docs can be "
                    f"set with the env variable 'RETRIEVAL_DOCS_DIR')."
                )
            log.info(
                f"Chunking reference PDF for {self.language} using unstructured - "
                f"if your PDF has many pages, this could take a while..."
            )
            start_time = time.time()
            loader = UnstructuredLoader(
                pdf_path,
                chunking_strategy="basic",
                max_characters=1000000,
                include_orig_elements=False,
                start_page=self.start_page,
                end_page=self.end_page,
            )
            docs = loader.load()
            text = "\n\n".join([doc.page_content for doc in docs])
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            documents = text_splitter.split_text(text)
            log.info(f"Document store created for language: {self.language}")
            end_time = time.time()
            log.info(
                f"Processing time for {self.language} PDF: "
                f"{end_time - start_time} seconds"
            )

            joblib.dump(documents, pickled_documents_path)
            log.debug(f"Documents saved to {pickled_documents_path}")

        return documents

    def vectorize_documents(self) -> (TfidfVectorizer, any):
        doc_vectors = self.vectorizer.fit_transform(self.documents)
        return doc_vectors

    def search_language_reference(
        self,
        query: List[str],
        top_k: int = 1,
        min_similarity: float = 0.1,
    ) -> List[Document]:
        """Searches through the vectorized PDF for the query using
        tf-idf and returns a list of langchain Documents."""

        docs: List[Document] = []

        for item in query:
            # Transform the query using the TF-IDF vectorizer
            query_vector = self.vectorizer.transform([item])

            # Calculate cosine similarities between the query and document vectors
            similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()

            # Get the indices of documents with similarity above the threshold
            valid_indices = [
                i for i, sim in enumerate(similarities) if sim >= min_similarity
            ]

            # Sort the valid indices by similarity score in descending order
            sorted_indices = sorted(
                valid_indices, key=lambda i: similarities[i], reverse=True
            )

            # Limit to top-k results
            top_indices = sorted_indices[:top_k]

            # Retrieve the top-k most relevant documents
            docs += [Document(page_content=self.documents[i]) for i in top_indices]
            log.debug(f"Langauge documentation search result: {docs}")

        return docs
