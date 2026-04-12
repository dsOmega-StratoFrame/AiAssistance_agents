from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, override

import pandas as pd
from langchain_core.documents import Document
from tqdm import tqdm


class DataSource(ABC):
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

    @override
    def get_item_id(self, item: Any) -> str | None:
        return item.id

    def add_documents(self, data):
        documents = []
        ids = []

        for i, item in tqdm(enumerate(data), total=len(data)):
            document = self.item_to_document(item)
            id = self.get_item_id(item) or str(i)
            ids.append(id)
            documents.append(document)

        return documents, ids


class DataFrameSource(DataSource, metaclass=ABCMeta):
    """DataSource implementation that works with pandas DataFrames."""

    def __init__(self, data_path: Path):
        self.data_path = data_path

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

    @override
    def get_item_id(self, item: pd.Series) -> str | None:
        return item.id

    # QUESTION: Just return iterator?
    @override
    def add_documents(self, data: pd.DataFrame):
        documents = []
        ids = []

        # TODO: Do we have better way to add?
        # https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
        for i, item in tqdm(data.iterrows(), total=data.rows):
            document = self.item_to_document(item)
            id = self.get_item_id(item) or str(i)
            ids.append(id)
            documents.append(document)

        return documents, ids
