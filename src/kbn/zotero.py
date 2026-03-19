from pyzotero import Zotero

IS_DEBUG = True

type TCollectionKey = str

LIBRARY_ID = "0"

def get_library_name(library_id):
    if library_id == "0":
        return "Library"

    raise NotImplementedError('Fetch library name for non-default libraries')


# Require Zotero 7+ with local API access enabled:
# Zotero > Settings > Advanced > "Allow other applications on this computer to communicate with Zotero".
zot = Zotero(library_id=LIBRARY_ID, library_type="user", local=True)

items = zot.top(limit=5)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for c in items:
    # print(item['data'])
    print(f"Item: {c['data'].get('title')}")


# [ {key, data, ...} ]
collections = zot.collections(limit=2000)
# { key: data }
collections_map = {}

for c in collections:
    collections_map[c['key']] = c['data']
    print(c['key'], c['data']['name'], c['data']['parentCollection'])
    # print(f"Item: {c['data']['title']}")

# Collection utils.
def get_name(key: TCollectionKey) -> str:
    return collections_map.get(key, { 'name': get_library_name(LIBRARY_ID) })['name']

def format_segments_as_path(path_segments: list[TCollectionKey]) -> str:
    path = [get_name(segment) for segment in path_segments]

    return '/'.join(path)

print(len(collections))

# { key: parentKey }
tree = {}

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
def construct_paths_structure():
    for c in collections:
        parentKey = c['data']['parentCollection']
        if not parentKey:
            if IS_DEBUG:
                print('no parent', c)
            tree[c['key']] = [get_library_name(LIBRARY_ID)]
        else:
            tree[c['key']] = [parentKey]

    for [parent, branch] in tree.items():
        if IS_DEBUG:
            print(f"{get_name(parent)} ({parent}): {format_segments_as_path(branch)} ({branch})")
        last_leaf = branch[-1]

        child_branch = tree.get(last_leaf)
        while child_branch:
            tree[parent] += child_branch

            last_leaf = child_branch[-1]
            child_branch = tree.get(last_leaf)

construct_paths_structure()


def debug():
    collections_paths = []

    for [parent, branch] in tree.items():
        path_segments = [parent] + branch
        path_segments.reverse()

        path = format_segments_as_path(path_segments)
        collections_paths.append(path)

        print(f"{path} | {parent}: {branch}")

    collections_paths.sort()
    print('------ sorted paths -----')
    for path in collections_paths:
        print(path)

if IS_DEBUG:
    debug()

# print(tree)
