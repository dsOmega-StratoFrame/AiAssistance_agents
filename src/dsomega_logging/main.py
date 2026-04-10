import logging
from pathlib import Path

from rich.logging import RichHandler

LOGS_PATH = Path("logs")

LOGS_PATH.mkdir(exist_ok=True)

FORMAT = "%(message)s"


logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[]
)

# Create file handler which logs even debug messages.
file_handler = logging.FileHandler(LOGS_PATH / "zotero.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Create console handler with a higher log level.
cli_handler = RichHandler()
cli_handler.setLevel(logging.ERROR)


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Add the handlers to the logger.
    log.addHandler(file_handler)
    log.addHandler(cli_handler)

    return log

log = get_logger("general")
