from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, override

from langchain_core.embeddings import Embeddings
import pandas as pd
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class DataSource(ABC):
    def __init__(self, data_path: Path, db_path: Path):
        self.data_path = data_path
        self.db_path = db_path

    @abstractmethod
    def load_data(self) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """Load data from the source. Returns data in a format suitable for processing."""
        pass

    @abstractmethod
    def item_to_document(
        self, item: Any  # pyright: ignore[reportExplicitAny, reportAny]
    ) -> Document:
        """Convert a single item of data to a Document."""
        pass

    @property
    def collection_name(self) -> str:
        return self.__class__.__name__.lower()

    # REFACTOR: Into separate class that is more about ml rather than data
    # source. Consider some pattern
    def get_vector_store(self, embeddings: Embeddings):
        from langchain_chroma import Chroma

        vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=str(self.db_path),
            embedding_function=embeddings,
        )

        return vector_store

    def add_documents(self, data):
        documents = []
        ids = []

        for i, item in enumerate(data):
            document = self.item_to_document(item)
            ids.append(document.id or str(i))
            documents.append(document)

        return documents, ids

    def get_retriever(self, embeddings: Embeddings, search_kwargs=None, add_documents=True) -> VectorStoreRetriever:
        vector_store = self.get_vector_store(embeddings=embeddings)

        # if not self.db_path.exists():
        data = self.load_data()

        if add_documents:
            # REFACTOR: May have trouble with batch add.
            documents, ids = self.add_documents(data)

        vector_store.add_documents(documents=documents, ids=ids)

        return vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 10})


class DataFrameSource(DataSource, metaclass=ABCMeta):
    """DataSource implementation that works with pandas DataFrames."""

    @abstractmethod
    @override
    def load_data(self) -> pd.DataFrame:
        """Load data as a pandas DataFrame."""
        return pd.read_csv(self.data_path)

    @abstractmethod
    @override
    def item_to_document(self, item: pd.Series) -> Document:
        """Convert a pandas Series row to a Document."""
        pass

    # QUESTION: Just return iterator?
    @override
    def add_documents(self, data: pd.DataFrame):
        documents = []
        ids = []

        # TODO: Do we have better way to add?
        # https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
        for i, item in data.iterrows():
            document = self.item_to_document(item)
            ids.append(document.id or str(i))
            documents.append(document)

        return documents, ids
