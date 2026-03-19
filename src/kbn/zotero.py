from pyzotero import Zotero

# Require Zotero 7+ with local API access enabled:
# Zotero > Settings > Advanced > "Allow other applications on this computer to communicate with Zotero".
zot = Zotero(library_id="0", library_type="user", local=True)

items = zot.top(limit=5)


# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for c in items:
    # print(item['data'])
    print(f"Item: {c['data']['title']}")


collections = zot.collections(limit=2000)
collections_map = {}

for c in collections:
    collections_map[c['key']] = c['data']
    print(c['key'], c['data']['name'], c['data']['parentCollection'])
    # print(f"Item: {c['data']['title']}")

print(len(collections))

tree = {}
result = {}
"""
parent can be `False` if the parent is the library root
{ parent: key }
Iterate through each entry. For each check additional structure:
{ lastLeaf: branch }

For example:
{
B: A(.B)
C: B(.C)
}
Check last of:
    B = first of A.B => A.B.C.
    C

"""
for c in collections:
    parentKey = c['data']['parentCollection']
    if not parentKey:
        print('no parent')
        tree['Library'] = [c['key']]
    else:
        tree[parentKey] = [c['key']]
    # del tree[False]
    # print(f"Item: {c['data']['title']}")

result = tree.pop('Library')

for [parent, branch] in tree.items():
    print(f"{parent}: {branch}")
    last_leaf = branch[-1]

    branch = tree.get(last_leaf)
    while branch:
        tree[parent] += branch

        last_leaf = branch[-1]
        branch = tree.get(last_leaf)

# for [parent, branch] in tree.items():
#     print(f"{parent}: {branch}")

collections_paths = []

for [parent, branch] in tree.items():
    path_segments = [parent] + branch

    path = [collections_map[segment]['name'] for segment in path_segments]

    path_str  = '/'.join(path)
    collections_paths.append(path_str)

    print(f"${path_str} | {parent}: {branch}")

collections_paths.sort()
print('------ sorted paths -----')
for path in collections_paths:
    print(path)

# print(tree)
# print(result)
