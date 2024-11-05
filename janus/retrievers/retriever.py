from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnableConfig

from janus.language.block import CodeBlock
from janus.llm.models_info import MODEL_PROMPT_ENGINES, JanusModel
from janus.utils.logger import create_logger
from janus.utils.pdf_docs_reader import PDFDocsReader

log = create_logger(__name__)


class JanusRetriever(Runnable):
    def __init__(self) -> None:
        super().__init__()

    def invoke(
        self, input: CodeBlock, config: RunnableConfig | None = None, **kwargs
    ) -> dict:
        kwargs.update(context=self.get_context(input))
        return kwargs

    def get_context(self, code_block: CodeBlock) -> str:
        return ""


class ActiveUsingsRetriever(JanusRetriever):
    def get_context(self, code_block: CodeBlock) -> str:
        context = "\n".join(
            f"{context_tag}: {context}"
            for context_tag, context in code_block.context_tags.items()
        )
        return f"You may use the following additional context: {context}"


class TextSearchRetriever(JanusRetriever):
    retriever: BaseRetriever

    def __init__(self, retriever: BaseRetriever):
        super().__init__()
        self.retriever = retriever

    def get_context(self, code_block: CodeBlock) -> str:
        if code_block.text is None:
            return ""
        docs = self.retriever.invoke(code_block.text)
        context = "\n\n".join(doc.page_content for doc in docs)
        return f"You may use the following additional context: {context}"


class LanguageDocsRetriever(JanusRetriever):
    def __init__(
        self,
        llm: JanusModel,
        language_name: str,
        prompt_template_name: str = "retrieval/language_docs",
    ):
        super().__init__()
        self.llm: JanusModel = llm
        self.language: str = language_name

        self.PDF_reader = PDFDocsReader(
            language=self.language,
        )

        language_docs_prompt = MODEL_PROMPT_ENGINES[self.llm.short_model_id](
            source_language=self.language,
            prompt_template=prompt_template_name,
        ).prompt

        parser: StrOutputParser = StrOutputParser()
        self.chain = language_docs_prompt | self.llm | parser

    def get_context(self, code_block: CodeBlock) -> str:
        functionality_to_reference: str = self.chain.invoke(
            dict({"SOURCE_CODE": code_block.text, "SOURCE_LANGUAGE": self.language})
        )
        if functionality_to_reference == "NODOCS":
            log.debug("No Opcodes requested from language docs retriever.")
            return ""
        else:
            functionality_to_reference: List = functionality_to_reference.split(", ")
            log.debug(
                f"List of opcodes requested by language docs retriever"
                f"to search the {self.language} "
                f"docs for: {functionality_to_reference}"
            )

            docs: List[Document] = self.PDF_reader.search_language_reference(
                functionality_to_reference
            )
            context = "\n\n".join(doc.page_content for doc in docs)
            if context:
                return (
                    f"You may reference the following excerpts from the {self.language} "
                    f"language documentation: {context}"
                )
            else:
                return ""
