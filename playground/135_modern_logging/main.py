
import atexit
import json
# import logging
import logging.config
import logging.handlers
import pathlib

from shared import *

# logging.info("hello") # BAD using root logger
logger = logging.getLogger("my_app")  # __name__ is a common choice

def setup_logging():
    config_file = HOME_DIR.joinpath("logging_configs", "2-stderr-json-file.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)
    # Queue Handler for Non-blocking Logging
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main():
    setup_logging()

    logging.basicConfig(level="INFO")
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
