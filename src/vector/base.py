from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

from data_sources.base import DataSource
from dsomega_logging.main import get_logger

log = get_logger("vector")


class VectorStoreManager:
    """Manages vector store operations."""

    def __init__(
        self,
        db_path: Path,
        collection_name: str,
        data_source: DataSource,
    ):

        self.data_source = data_source
        self._vector_store = None

        # Vector store.
        self.db_path = db_path
        self.collection_name = collection_name
        self.embedding_function = None

    @property
    def vector_store(self):
        if self._vector_store:
            return self._vector_store

        if not self.embedding_function:
            log.info("You may have used `vector_store` before running get_retriever")
            raise ValueError("self.embedding_function must be provided to use vector store")

        from langchain_chroma import Chroma

        self._vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=str(self.db_path),
            embedding_function=self.embedding_function,
        )

        return self._vector_store

    # # STYLE: Add typehint for vector_store.
    @vector_store.setter
    def vector_store(self, vector_store):
        self._vector_store = vector_store

    # TODO:Use adapter that translates DataSource data to Document. Provide
    # adapter to VectorStoreManager and create an adaptee.
    # class DataSourceAdapter
    def get_retriever(
        self,
        embedding_function: Embeddings,
        search_kwargs=None,
        add_documents=True,
    ) -> VectorStoreRetriever:
        # TODO:
        # if not self.db_path.exists():

        self.embedding_function = embedding_function
        data = self.data_source.load_data()

        if add_documents:
            # REFACTOR: May have trouble with batch add.
            documents, ids = self.data_source.add_documents(data)

            self.vector_store.add_documents(documents=documents, ids=ids)

        return self.vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 10})
