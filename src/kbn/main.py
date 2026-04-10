from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from kbn.vector import retriever
from kbn.zotero import construct_paths_structure, format_path_structure

model = OllamaLLM(model="qwen3.5:9b")

PIZZA_TEMPLATE = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {context}

Here is the question to answer: {question}
"""

TASKWARRIOR_TEMPLATE = """
You are an expert in time management and know very well how to prioritize tasks
to achieve best results longterm in IT and related fields.

When you reference a task, use it's id in full form.

Here are some relevant tasks: {context}

Here is the question to answer: {question}
"""

ZOTERO_TEMPLATE = """
You are an expert in library and references management and know very well
how to organize resources and data to achieve best results longterm in IT and related fields.

Here are some relevant collections: {context}

Here is the question to answer: {question}
"""

def select_template(template: string) -> ChatPromptTemplate:
    print("Following template:")
    print(template)

    return ChatPromptTemplate.from_template(template)


while True:
    print("\n\n-------------------------------")
    # TODO: In the future add here chat assistant too.
    user_input = input("Choose a program (h for help, q to quit): ")
    print("\n")
    get_context = None

    if user_input == "q":
        break

    elif user_input == "h" or user_input == "help":
        print("Available programs:")
        print("t - taskwarrior")
        print("z - zotero")
        print("p - pizza")

    elif user_input == "z" or user_input == "zotero":
        paths_structure = construct_paths_structure()

        formatted_paths_structure = format_path_structure(paths_structure)

        def get_context(_question: str) -> str:
            return formatted_paths_structure

        prompt = select_template(ZOTERO_TEMPLATE)
    elif user_input == "t" or user_input == "task" or user_input == "taskwarrior":
        def get_context(question: str) -> str:
            return retriever.invoke(question)

        prompt = select_template(TASKWARRIOR_TEMPLATE)
    elif user_input == "p" or user_input == "pizza":
        def get_context(question: str) -> str:
            return retriever.invoke(question)

        prompt = select_template(PIZZA_TEMPLATE)

    if not get_context:
        continue

    while True:
        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit to previous stage): ")
        chain = prompt | model

        if question == "q":
            break

        result = chain.invoke({
            "context": get_context(question),
            "question": question,
        })
        print(result)
