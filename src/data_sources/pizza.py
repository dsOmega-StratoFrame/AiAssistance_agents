from typing import Any, override

import pandas as pd
from langchain_core.documents import Document

from data_sources.base import DataFrameSource


class PizzaDataSource(DataFrameSource):
    @override
    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_path)

    @override
    def item_to_document(self, item):
        print(item)
        content = f"{item['Title']} {item['Review']}"
        metadata = {"rating": item["Rating"], "date": item["Date"]}

        return Document(page_content=content, metadata=metadata, id=str(item.name))
