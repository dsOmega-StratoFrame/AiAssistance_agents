from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from kbn.vector import retriever

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

template = TASKWARRIOR_TEMPLATE
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("Following template:")
print(template)

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    context = retriever.invoke(question)
    result = chain.invoke({
        "context": context,
        "question": question,
    })
    print(result)
