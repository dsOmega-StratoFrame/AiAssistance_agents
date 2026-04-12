from typing import Any, TypedDict


# --- General ---
class LinksDict(TypedDict, total=False):
    self: dict[str, Any]
    alternate: dict[str, Any]


class LibraryDict(TypedDict, total=False):
    type: str
    id: int
    name: str
    links: LinksDict


class MetaDict(TypedDict, total=False):
    creatorSummary: str
    parsedDate: str
    numChildren: int


type TRelations = dict[str, Any]


# --- Collections ---
class CollectionDataDict(TypedDict, total=False):
    key: str
    version: int
    name: str
    parentCollection: str | bool  # False or parent collection key
    relations: TRelations


class CollectionDict(TypedDict, total=False):
    key: str
    version: int
    library: LibraryDict
    links: LinksDict
    meta: MetaDict
    data: CollectionDataDict


# --- Item ---
class CreatorDict(TypedDict, total=False):
    firstName: str
    lastName: str
    creatorType: str


class TagsDict(TypedDict, total=False):
    tag: str
    type: int


type CollectionKey = str


class ItemDataDict(TypedDict, total=False):
    key: str
    version: int
    itemType: str
    title: str
    date: str
    shortTitle: str
    url: str
    accessDate: str
    citationKey: str
    forumTitle: str
    postType: str
    creators: list[CreatorDict]
    tags: list[TagsDict]
    collections: list[CollectionKey]
    relations: TRelations
    dateAdded: str
    dateModified: str


class ZoteroItemDict(TypedDict, total=False):
    key: str
    version: int
    library: LibraryDict
    links: LinksDict
    meta: MetaDict
    data: ItemDataDict
