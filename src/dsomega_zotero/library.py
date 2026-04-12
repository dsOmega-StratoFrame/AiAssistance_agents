from pyzotero import Zotero

from config.zotero import IS_LOCAL_LIBRARY, LIBRARY_ID


def get_library_name(library_id):
    if library_id == "0":
        return "Library"

    raise NotImplementedError("Fetch library name for non-default libraries")


# Require Zotero 7+ with local API access enabled:
# Zotero > Settings > Advanced > "Allow other applications on this computer to communicate with Zotero".
zot = Zotero(library_id=LIBRARY_ID, library_type="user", local=IS_LOCAL_LIBRARY)
