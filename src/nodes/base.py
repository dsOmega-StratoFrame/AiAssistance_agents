import sys

from abc import ABC, ABCMeta, abstractmethod
from typing import override

from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate

from vector.base import VectorStoreManager


class ChatNode(ABC):
    """Get context in any way possible."""

    @property
    @abstractmethod
    def template(self) -> str:
        pass

    @abstractmethod
    def get_context(self, question: str) -> str:
        pass

    def get_prompt(self) -> ChatPromptTemplate:
        if sys.stdin.isatty():
            print("Following template:")
            print(self.template)

        return ChatPromptTemplate.from_template(self.template)


class VectorRetrieverChatNode(ChatNode, metaclass=ABCMeta):
    """Get context using vector retriever."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager,
        embedding_function: Embeddings,
    ):
        self.vector_store_manager = vector_store_manager
        self.embedding_function = embedding_function

        self.retriever = None

    @property
    @override
    @abstractmethod
    def template(self) -> str:
        pass

    @override
    def get_context(self, question: str) -> str:
        self.retriever = self.retriever or self.vector_store_manager.get_retriever(
            embedding_function=self.embedding_function
        )

        return self.retriever.invoke(question)
