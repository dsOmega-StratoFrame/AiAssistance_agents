from typing import override

import pandas as pd
from langchain_core.documents import Document

from config.paths import pizza_raw_data_path
from data_sources.base import DataFrameSource


class PizzaDataSource(DataFrameSource):
    @override
    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_path)

    @override
    def get_item_id(self, item: pd.Series) -> str | None:
        return str(item.name)

    @override
    def item_to_document(self, item):
        content = f"{item['Title']} {item['Review']}"
        metadata = {"rating": item["Rating"], "date": item["Date"]}

        return Document(
            page_content=content, metadata=metadata, id=self.get_item_id(item)
        )


pizza_data_source = PizzaDataSource(data_path=pizza_raw_data_path)
