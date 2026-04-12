from typing import override

from langchain_core.documents import Document

from data_sources.base import DataSource
from dsomega_logging.main import get_logger
from dsomega_zotero.base import ZoteroItemDict
from dsomega_zotero.collections import get_collections_view
from dsomega_zotero.items import (format_item_collections,
                                  format_item_creators, format_item_tags,
                                  get_items, item_url)

log = get_logger("data_sources__zotero")


class ZoteroDataSource(DataSource):
    def __init__(self) -> None:
        super().__init__()
        self._collections_view = None
        self._collections_paths = None
        self._collections_path_map = None

    @override
    def load_data(self):
        return get_items()

    @override
    def get_item_id(self, item: ZoteroItemDict) -> str | None:
        return item_url(item)

    @property
    def collections_view(self):
        if self._collections_view:
            return self._collections_view

        self._collections_view = get_collections_view()

        return self._collections_view

    @property
    def collections_paths(self):
        if self._collections_paths:
            return self._collections_paths

        if not self.collections_view:
            msg = "Method `collections_paths` was used before `collections_view` was initialized."
            log.error(msg)
            log.info("Check that `get_collections_view` is working")
            raise ValueError(msg)

        self._collections_paths = self.collections_view.construct_paths_structure()

        return self._collections_paths

    @property
    def collections_path_map(self):
        if self._collections_path_map:
            return self._collections_path_map

        if not self.collections_view:
            msg = "Method `collections_paths` was used before `collections_view` was initialized."
            log.error(msg)
            log.info("Check that `get_collections_view` is working")
            raise ValueError(msg)

        self._collections_path_map = \
            self.collections_view.format_paths_structure_as_map(self.collections_paths)

        return self._collections_path_map

    @override
    def item_to_document(self, item: ZoteroItemDict):
        data = item.get("data", {})

        metadata = {field: data.get(field, "") for field in [
            "itemType",
            "shortTitle",
            "url",
            "accessDate",
            "citationKey",
            "dateAdded",
            "dateModified",
        ]}
        metadata["select_url"] = item_url(item)

        if not self.collections_path_map:
            msg = "Method `collections_path_map` was used before `collections_view` was initialized."
            log.error(msg)
            log.info("Check that `get_collections_view` is working")
            raise ValueError(msg)

        collections = format_item_collections(item, self.collections_path_map)
        if collections and len(collections):
            metadata["collections"] = collections

        creators = format_item_creators(item)
        if len(creators):
            metadata["creators"] = creators

        page_content = "Empty"

        try:
            page_content = item.get("wikipedia").strip("{} ") or \
                data.get("title") or \
                data.get("shortTitle") or \
                f"{data.get("itemType")}: {data.get("url")}"
        except Exception as e:
            log.error(f"Error generating page_content for document {e}")
            log.debug(data)

        if (isinstance(data.get("tags"), list) and len(data.get("tags"))):
            page_content += f" {format_item_tags(item)}"

        # if (isinstance(item.get("annotations"), list) and len(item["annotations"])):
        #     anotations_body = "\n".join([
        #          f"{ann["entry"]}: {ann["description"]}" for ann in item.get("annotations")
        #     ])
        #     page_content += "\n" + anotations_body

        id = self.get_item_id(item)

        document = Document(
            page_content=page_content,
            metadata=metadata,
            id=id
        )

        return document


zotero_data_source = ZoteroDataSource()
