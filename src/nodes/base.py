template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {context}

Here is the question to answer: {question}
"""

def get_context(question: str) -> str:
    return retriever.invoke(question)

prompt = select_template(PIZZA_TEMPLATE)

class ChatNode:
    
