from typing import Any, TypedDict


class CreatorDict(TypedDict, total=False):
    firstName: str
    lastName: str
    creatorType: str


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
    tags: list[Any]
    collections: list[Any]
    relations: dict[str, Any]
    dateAdded: str
    dateModified: str


class ZoteroItemDict(TypedDict, total=False):
    key: str
    version: int
    library: LibraryDict
    links: LinksDict
    meta: MetaDict
    data: ItemDataDict
