from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

# from kbn.zotero import construct_paths_structure, format_path_structure
from nodes.base import ChatNode
from nodes.pizza import PizzaChatNode, pizza_vector_store_manager
from nodes.taskwarrior import TaskwarriorChatNode, taskwarrior_vector_store_manager

model = OllamaLLM(model="qwen3.5:9b")

embedding_function = OllamaEmbeddings(model="qwen3-embedding:4b")

ZOTERO_TEMPLATE = """
You are an expert in library and references management and know very well
how to organize resources and data to achieve best results longterm in IT and related fields.

Here are some relevant collections: {context}

Here is the question to answer: {question}
"""


while True:
    print("\n\n-------------------------------")
    # TODO: In the future add here chat assistant too.
    user_input = input("Choose a program (h for help, q to quit): ")
    print("\n")
    # get_context = None
    node: ChatNode | None = None

    if user_input == "q":
        break

    elif user_input == "h" or user_input == "help":
        print("Available programs:")
        print("t - taskwarrior")
        print("z - zotero")
        print("p - pizza")

    # elif user_input == "z" or user_input == "zotero":
    #     paths_structure = construct_paths_structure()

    #     formatted_paths_structure = format_path_structure(paths_structure)

    #     def get_context(_question: str) -> str:
    #         return formatted_paths_structure

    #     prompt = select_template(ZOTERO_TEMPLATE)
    elif user_input == "t" or user_input == "task" or user_input == "taskwarrior":
        taskwarrior_chat_node = TaskwarriorChatNode(
            vector_store_manager=taskwarrior_vector_store_manager,
            embedding_function=embedding_function,
        )
        node = taskwarrior_chat_node
        prompt = node.get_prompt()
    elif user_input == "p" or user_input == "pizza":
        pizza_chat_node = PizzaChatNode(
            vector_store_manager=pizza_vector_store_manager,
            embedding_function=embedding_function,
        )
        node = pizza_chat_node
        prompt = node.get_prompt()

    if not node:
        continue

    while True:
        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit to previous stage): ")
        chain = prompt | model

        if question == "q":
            break

        result = chain.invoke(
            {
                "context": node.get_context(question),
                "question": question,
            }
        )
        print(result)
