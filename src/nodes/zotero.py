from typing import override

from config.paths import zotero_db_path
from data_sources.zotero import zotero_data_source
from nodes.base import VectorRetrieverChatNode
from vector.base import VectorStoreManager


class ZoteroChatNode(VectorRetrieverChatNode):
    @property
    @override
    def template(self):
        return """
        You are an expert in library and references management and know very well
        how to organize resources and data to achieve best results longterm in IT and related fields.

        Here are some relevant collections: {context}

        Here is the question to answer: {question}
        """


zotero_vector_store_manager = VectorStoreManager(
    db_path=zotero_db_path,
    collection_name="zotero",
    data_source=zotero_data_source,
)
