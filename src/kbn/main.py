from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

# from kbn.zotero import construct_paths_structure, format_path_structure
from dsomega_logging.console import console
from dsomega_logging.main import get_logger
from nodes.base import ChatNode
from nodes.pizza import PizzaChatNode, pizza_vector_store_manager
from nodes.taskwarrior import TaskwarriorChatNode, taskwarrior_vector_store_manager
from rich.markdown import Markdown
from rich.prompt import Prompt

model = OllamaLLM(model="qwen3.5:9b")

embedding_function = OllamaEmbeddings(model="qwen3-embedding:4b")

ZOTERO_TEMPLATE = """
You are an expert in library and references management and know very well
how to organize resources and data to achieve best results longterm in IT and related fields.

Here are some relevant collections: {context}

Here is the question to answer: {question}
"""

log = get_logger("chat")

# def initialize_vector_stores():
#     """Initialize vector stores with data on first run only."""
#     # Initialize pizza vector store
#     pizza_vector_store_manager.get_retriever(
#         embedding_function=embedding_function,
#         add_documents=True,
#     )
#     
#     # Initialize taskwarrior vector store
#     taskwarrior_vector_store_manager.get_retriever(
#         embedding_function=embedding_function,
#         add_documents=True,
#     )


# # Initialize vector stores once at startup
# initialize_vector_stores()


while True:
    print("\n\n-------------------------------")
    # TODO: In the future add here chat assistant too.
    user_input = Prompt.ask("Choose a program (h for help, q to quit)")
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
        node = TaskwarriorChatNode(
            vector_store_manager=taskwarrior_vector_store_manager,
            embedding_function=embedding_function,
        )
    elif user_input == "p" or user_input == "pizza":
        node = PizzaChatNode(
            vector_store_manager=pizza_vector_store_manager,
            embedding_function=embedding_function,
        )

    if not node:
        continue

    prompt = node.get_prompt()

    while True:
        print("\n\n-------------------------------")
        question = Prompt.ask("Ask your question (q to quit to previous stage)")
        chain = prompt | model

        if question == "q":
            break

        status_msg = f"Processing question with {model.get_name()}/{model.model}..."
        log.info(status_msg)
        with console.status(status_msg):
            result = chain.invoke(
                {
                    "context": node.get_context(question),
                    "question": question,
                }
            )
            log.info(result)
            console.print(Markdown(result))
