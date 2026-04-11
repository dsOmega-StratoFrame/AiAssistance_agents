from typing import override

from config.paths import pizza_db_path
from data_sources.pizza import pizza_data_source
from nodes.base import VectorRetrieverChatNode
from vector.base import VectorStoreManager


class PizzaChatNode(VectorRetrieverChatNode):
    @property
    @override
    def template(self):
        return """
        You are an expert in answering questions about a pizza restaurant

        Here are some relevant reviews: {context}

        Here is the question to answer: {question}
        """


pizza_vector_store_manager = VectorStoreManager(
    db_path=pizza_db_path,
    collection_name="restaurant_reviews",
    data_source=pizza_data_source,
)
