from typing import override

from config.paths import taskwarrior_db_path
from data_sources.taskwarrior import taskwarrior_data_source
from nodes.base import VectorRetrieverChatNode
from vector.base import VectorStoreManager


class TaskwarriorChatNode(VectorRetrieverChatNode):
    @property
    @override
    def template(self):
        return """
        You are an expert in time management and know very well how to prioritize tasks
        to achieve best results longterm in IT and related fields.

        When you reference a task, use it's id in full form.

        Here are some relevant tasks: {context}

        Here is the question to answer: {question}
        """


taskwarrior_vector_store_manager = VectorStoreManager(
    db_path=taskwarrior_db_path,
    collection_name="taskwarrior",
    data_source=taskwarrior_data_source,
)
