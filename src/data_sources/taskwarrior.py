from typing import override

import pandas as pd
from langchain_core.documents import Document

from config.paths import taskwarrior_raw_data_path
from data_sources.base import DataFrameSource


class TaskwarriorDataSource(DataFrameSource):
    @override
    def load_data(self) -> pd.DataFrame:
        return pd.read_json(self.data_path)

    @override
    def get_item_id(self, item: pd.Series) -> str | None:
        return str(item["uuid"])

    def item_to_document(self, item):
        metadata = item[[
            "urgency",
            "priority",
            "status",
            "due",
            "wait",
            "start",
            # "end",
            "project",
            "depends",
        ]].dropna()

        item = item.dropna()
        # print(row)
        page_content = item.get("logseqtitle") or item["description"]

        if (isinstance(item.get("tags"), list) and len(item.get("tags"))):
            tags = " ".join(map(lambda t: "#" + t, item.get("tags")))
            # print(page_content)
            # print(tags)
            page_content += f" {tags}"

        if (isinstance(item.get("annotations"), list) and len(item["annotations"])):
            anotations_body = "\n".join([
                 f"{ann["entry"]}: {ann["description"]}" for ann in item.get("annotations")
            ])
            page_content += "\n" + anotations_body

        id = self.get_item_id(item)

        document = Document(
            page_content=page_content,
            metadata=metadata.to_dict(),
            id=id
        )

        return document


taskwarrior_data_source = TaskwarriorDataSource(
    data_path=taskwarrior_raw_data_path
)
