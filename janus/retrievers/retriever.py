from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnableConfig

from janus.language.block import CodeBlock


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
