from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
from langchain_core.documents import Document


class DataSource(ABC):
    def __init__(self, data_path: Path, db_path: Path):
        self.data_path = data_path
        self.db_path = db_path

    @abstractmethod
    def load_dataframe(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def row_to_document(self, row: pd.Series) -> Document:
        pass

    @property
    def collection_name(self) -> str:
        return self.__class__.__name__.lower()

    def get_retriever(self, embeddings, search_kwargs=None):
        from langchain_chroma import Chroma

        vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=str(self.db_path),
            embedding_function=embeddings,
        )
        if not self.db_path.exists():
            df = self.load_dataframe()
            documents = []
            ids = []
            for idx, row in df.iterrows():
                doc = self.row_to_document(row)
                documents.append(doc)
                ids.append(doc.id or str(idx))  # ensure id
            vector_store.add_documents(documents=documents, ids=ids)
        return vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 10})
