import logging
from datetime import datetime
from pathlib import Path

from rich.logging import RichHandler

LOGS_PATH = Path("logs")
COMMON_LOGS_PATH = LOGS_PATH / "common"

LOGS_PATH.mkdir(exist_ok=True)
COMMON_LOGS_PATH.mkdir(exist_ok=True)

FORMAT = "%(message)s"


logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[])

# Create console handler with a higher log level.
cli_handler = RichHandler()
cli_handler.setLevel(logging.ERROR)


# Reference: https://stackoverflow.com/a/28147286/24067232
def date_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


common_file_handler = logging.FileHandler(COMMON_LOGS_PATH / f"{date_iso()}.log")


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Create file handler which logs even debug messages.
    file_handler = logging.FileHandler(LOGS_PATH / f"{name}.log")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger.
    log.addHandler(common_file_handler)
    log.addHandler(file_handler)
    log.addHandler(cli_handler)

    return log


log = get_logger("general")
