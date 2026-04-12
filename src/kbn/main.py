from argparse import RawDescriptionHelpFormatter

from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from rich.markdown import Markdown
from rich.prompt import Prompt
from tap import Tap

# from kbn.zotero import construct_paths_structure, format_path_structure
from dsomega_logging.console import console
from dsomega_logging.main import get_logger
from nodes.base import ChatNode
from nodes.pizza import PizzaChatNode, pizza_vector_store_manager
from nodes.taskwarrior import (TaskwarriorChatNode,
                               taskwarrior_vector_store_manager)
from nodes.zotero import ZoteroChatNode, zotero_vector_store_manager

model = OllamaLLM(model="qwen3.5:9b")

embedding_function = OllamaEmbeddings(model="qwen3-embedding:4b")

log = get_logger("chat")


class ArgumentParser(Tap):
    agent: str = "taskwarrior"  # Select which agent to run.
    prompt: str | None = None  # Question to ask.


def parse_args():
    """Parse CLI arguments using argparse and tap."""
    parser = ArgumentParser(
        description="System of agents to interact with Knowledge Base",
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s                 # Start interactive chat.
  %(prog)s --agent pizza # Start a chat with preselected agent.
  %(prog)s --agent zotero --prompt "Select references about pandas" # Non-interactive usage
  """,
    )

    return parser.parse_args()


args = parse_args()


def select_node(user_input: str) -> ChatNode | None:
    if user_input in ["zotero", "z"]:
        #     paths_structure = construct_paths_structure()

        #     formatted_paths_structure = format_path_structure(paths_structure)

        #     def get_context(_question: str) -> str:
        #         return formatted_paths_structure

        #     prompt = select_template(ZOTERO_TEMPLATE)
        return ZoteroChatNode(
            vector_store_manager=zotero_vector_store_manager,
            embedding_function=embedding_function,
        )
    elif user_input in ["taskwarrior", "task", "t"]:
        return TaskwarriorChatNode(
            vector_store_manager=taskwarrior_vector_store_manager,
            embedding_function=embedding_function,
        )
    elif user_input in ["pizza", "p"]:
        return PizzaChatNode(
            vector_store_manager=pizza_vector_store_manager,
            embedding_function=embedding_function,
        )


interaction_count = {
    "agent": -1,
    "prompt": -1,
}


while True:
    interaction_count["agent"] += 1

    if interaction_count["agent"] == 0 and args.agent:
        node = select_node(args.agent)
    else:
        print("\n\n-------------------------------")
        # TODO: In the future add here chat assistant too.
        user_input = Prompt.ask("Choose a program (h for help, q to quit)")
        print("\n")
        # get_context = None
        node: ChatNode | None = None

        if user_input == "q":
            break

        elif user_input in ["help", "h"]:
            print("Available programs:")
            print("t - taskwarrior")
            print("z - zotero")
            print("p - pizza")

        node = select_node(user_input)

    if not node:
        continue

    prompt_template = node.get_prompt()

    while True:
        interaction_count["prompt"] += 1

        print("\n\n-------------------------------")

        prompt = ""

        if interaction_count["prompt"] == 0 and args.prompt:
            prompt = args.prompt
        else:
            prompt = Prompt.ask("Ask your question (q to quit to previous stage)")

            if prompt == "q":
                break

        chain = prompt_template | model

        status_msg = f"Processing question with {model.get_name()}/{model.model}..."
        log.info(status_msg)
        with console.status(status_msg):
            result = chain.invoke(
                {
                    "context": node.get_context(prompt),
                    "question": prompt,
                }
            )
            log.info(result)
            console.print(Markdown(result))
