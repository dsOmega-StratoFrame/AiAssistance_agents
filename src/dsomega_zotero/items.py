from functools import reduce
import sys

import httpx

from config.zotero import ITEMS_LIMIT
from dsomega_logging.main import get_logger
from dsomega_zotero.base import CreatorDict, ZoteroItemDict
from dsomega_zotero.collections import TCollectionsPathMap
from dsomega_zotero.library import IS_LOCAL_LIBRARY, zot

log = get_logger("zotero__items")


def get_items():
    items = []

    try:
        # items = zot.top(
        # style='chicago-note-bibliography',
        # [ {key, data, wikipedia, ...} ]
        # https://www.zotero.org/support/dev/web_api/v3/basics#export_formats
        items = zot.items(
            limit=ITEMS_LIMIT,
            format='json',
            include="data,wikipedia"
        )

        log.debug(f"First 5 items from collection:\n{items[:5]}")
    except httpx.ConnectError as e:
        log.debug(e)
        msg = f"Make sure Zotero is available."
        if IS_LOCAL_LIBRARY:
            msg += "\nCheck that Zotero app is running locally."

        log.error(msg)
        sys.exit(1)

    return items
    # return [format_item(item) for item in items]


# TODO: Add support for group library keys. For instance:
# "zotero://select/groups/6065865/items/@IdentitySciPyV1161"
def item_url(item: ZoteroItemDict):
    data = item.get("data", {})
    citationKey = data.get("citationKey")
    if citationKey:
        return f"zotero://select/library/items/@{citationKey}"

    return f"zotero://select/library/items/{data.get("key")}"


def format_item_collections(item: ZoteroItemDict, collections_path_map: TCollectionsPathMap):
    data = item.get("data", {})

    collections = data.get("collections", [])

    def get_collection_path(paths: list[str], key: str):
        collection = collections_path_map.get(key)

        if not collection:
            msg = f"Haven't found collection with {key} in `collections_path_map` even though item exists in a collection with this key"
            log.error(msg)
            raise ValueError(msg)

        paths.append(key)

        return paths

    paths = reduce(get_collection_path, collections, [])

    return paths


def format_creator(creator: CreatorDict):
    last_name = creator.get("lastName")
    first_name = creator.get("firstName")
    if last_name:
        if first_name:
            return f"{last_name} {first_name}"

        return last_name

    if first_name:
        return first_name

    log.warning(
        f"Got a creator item without both lastName and firstName: {creator}"
    )

    return ""


def format_item_creators(item: ZoteroItemDict):
    data = item.get("data", {})

    creators = data.get("creators", [])

    return [format_creator(c) for c in creators]


def format_item_tags(item: ZoteroItemDict):
    data = item.get("data", {})

    return " ".join(map(lambda t: "#" + t.get("tag", ""), data.get("tags", [])))
