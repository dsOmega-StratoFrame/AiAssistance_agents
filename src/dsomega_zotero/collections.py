import sys

import httpx

from config.zotero import COLLECTIONS_LIMIT, IS_LOCAL_LIBRARY
from dsomega_logging.main import get_logger
from dsomega_zotero.base import CollectionDataDict
from dsomega_zotero.library import LIBRARY_ID, get_library_name, zot

IS_DEBUG = False

log = get_logger("zotero__collections")

type TCollectionKey = str
type TCollectionsList = list[CollectionDataDict]
type TCollectionsMap = dict[TCollectionKey, CollectionDataDict]


def get_collections():
    collections: TCollectionsList = []

    try:
        # [ {key, data, ...} ]
        collections = zot.collections(limit=COLLECTIONS_LIMIT)

        return collections
    except httpx.ConnectError as e:
        log.debug(e)
        msg = "Make sure Zotero is available."
        if IS_LOCAL_LIBRARY:
            msg += "\nCheck that Zotero app is running locally."

        log.error(msg)
        sys.exit(1)


def get_collections_map():
    collections = get_collections()

    return CollectionsMap(collections)


def get_collections_view():
    collections = get_collections()

    return CollectionsView(collections)


class CollectionsMap:
    """Container for Zotero collection data with helper methods."""

    def __init__(self, collections: TCollectionsList) -> None:
        # { key: data }
        collections_map: TCollectionsMap = {}

        for c in collections:
            collections_map[c["key"]] = c[
                "data"
            ]  # pyright: ignore[reportTypedDictNotRequiredAccess]

        self._map = collections_map

    def __getitem__(self, key: TCollectionKey) -> CollectionDataDict:
        """Allow direct access to collection data via indexing."""
        return self._map[key]

    def get(
        self, key: TCollectionKey, default: CollectionDataDict | None = None
    ) -> CollectionDataDict | None:
        """Optional dict-like get method."""
        return self._map.get(key, default)

    def __contains__(self, key: TCollectionKey) -> bool:
        return key in self._map

    def get_name(self, key: TCollectionKey) -> str:
        """Return the name of a collection by its key."""
        data = self._map.get(key)
        if data:
            return data.get("name", "")
        return get_library_name(LIBRARY_ID)

    def format_segments_as_path(self, path_segments: list[TCollectionKey]) -> str:
        """Convert a list of collection keys into a slash-separated path string."""
        path = [self.get_name(segment) for segment in path_segments]

        return "/".join(path)


type TCollectionsPathMap = dict[TCollectionKey, str]


class CollectionsView(CollectionsMap):
    """Aggregator of collections raw data into more easy-to-use data structures."""

    def __init__(self, collections: TCollectionsList) -> None:
        super().__init__(collections)
        self.collections = collections

    def construct_paths_structure(self):
        """
        Parent can be `False` if the parent is the library root
        { key: parent }
        Iterate through each entry. For each construct additional structure:
        { key: branch }

        For example, for Zotero structure:
            Library/A/B1
            Library/A/B2/C
        Do the following:
            {
                A: [Library],
                B1: [A],
                B2: [A],
                C: [B2],
            }
            Check last leaf of each branch and try to connect with other existing branch:
                - For A it will be [Library]. Last leaf is 'Library'. There's no entries by key 'Library'
                - For B1 it will be [A]. Last leaf is 'A'. There's an entry `A: [Library]`. Merge them
                  and get:
                    {
                        A: [Library],
                        B1: [A, Library],
                        B2: [A],
                        C: [B2],
                    }
                ...and so on until you get:
                    {
                        A: [Library],
                        B1: [A, Library],
                        B2: [A, Library],
                        C: [B2, A, Library],
                    }

        As you can se, result is reversed.
        """

        # { key: parentKey }
        tree = {}

        for c in self.collections:
            parentKey = c["data"][
                "parentCollection"
            ]  # pyright: ignore[reportGeneralTypeIssues]
            if not parentKey:
                if IS_DEBUG:
                    print("no parent", c)
                tree[c["key"]] = [
                    get_library_name(LIBRARY_ID)
                ]  # pyright: ignore[reportTypedDictNotRequiredAccess]
            else:
                tree[c["key"]] = [
                    parentKey
                ]  # pyright: ignore[reportTypedDictNotRequiredAccess]

        for [parent, branch] in tree.items():
            if IS_DEBUG:
                print(
                    f"{self.get_name(parent)} ({parent}): {self.format_segments_as_path(branch)} ({branch})"
                )
            last_leaf = branch[-1]

            child_branch = tree.get(last_leaf)
            while child_branch:
                tree[parent] += child_branch

                last_leaf = child_branch[-1]
                child_branch = tree.get(last_leaf)

        return tree

    def format_paths_structure_as_list(self, paths_structure) -> list[str]:
        collections_paths = []

        for [parent, branch] in paths_structure.items():
            path_segments = [parent] + branch
            path_segments.reverse()

            path = self.format_segments_as_path(path_segments)
            collections_paths.append(path)

            if IS_DEBUG:
                print(f"{path} | {parent}: {branch}")

        return collections_paths

    def format_paths_structure_for_context(self, paths_structure) -> str:
        """["Library/full/path/A", "Library/full/path/B"]"""
        collections_paths = self.format_paths_structure_as_list(paths_structure)

        collections_paths.sort()

        return "\n".join(collections_paths)

    def format_paths_structure_as_map(self, paths_structure) -> TCollectionsPathMap:
        """
        {
          "KeyOfA": "Library/full/path/A",
          "KeyOfB": "Library/full/path/B"
        }
        """
        collections_paths = {}

        for [parent, branch] in paths_structure.items():
            path_segments = [parent] + branch
            path_segments.reverse()

            path = self.format_segments_as_path(path_segments)
            collections_paths[parent] = path

            if IS_DEBUG:
                print(f"{path} | {parent}: {branch}")

        return collections_paths


if __name__ == "__main__":
    print("--- Collections ---")
    collections_view = get_collections_view()
    for c in collections_view.collections:
        print(c["key"], c["data"]["name"], c["data"]["parentCollection"])

    print("Number of collections: ", len(collections_view.collections))

    paths_structure = collections_view.construct_paths_structure()
    # print(paths_structure)

    print("------ Map with full paths for each collection -----")
    formatted_paths_structure = collections_view.format_paths_structure_as_map(
        paths_structure
    )
    print(formatted_paths_structure)

    print("------ Sorted paths -----")
    print(formatted_paths_structure)
