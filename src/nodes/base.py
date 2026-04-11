from abc import ABC, abstractmethod
from typing import Callable, override

from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever

from data_sources.base import DataSource


class ChatNode(ABC):
    """Get context in any way possible."""

    @property
    @abstractmethod
    def template(self) -> str:
        pass

    @abstractmethod
    def get_context_factory(self, question: str) -> str:
        pass

    def get_prompt(self) -> ChatPromptTemplate:
        print("Following template:")
        print(self.template)

        return ChatPromptTemplate.from_template(self.template)


class VectorRetrieverChatNode(ChatNode, metaclass=ABC):
    """Get context using vector retriever."""

    def __init__(
        self,
        data_source: DataSource,
        retriever: VectorStoreRetriever,
    ):
        self.data_source = data_source
        self.retriever = retriever

    @property
    @override
    @abstractmethod
    def template(self) -> str:
        pass

    @override
    def get_context_factory(self, embeddings: Embeddings) -> Callable[[str], str]:
        retriever = self.data_source.get_retriever(embeddings=embeddings)

        def get_context(question: str) -> str:
            return retriever.invoke(question)

        return get_context

    def get_prompt(self) -> ChatPromptTemplate:
        print("Following template:")
        print(self.template)

        return ChatPromptTemplate.from_template(self.template)
