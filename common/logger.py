import logging
import sys


def create_logger():

    logger = logging.getLogger("klm_homework")
    logger.propagate = False
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(filename)s %(funcName)s %(lineno)s - %(message)s",
        level=logging.INFO,
    )

    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Adding a StreamHandler to push the messages to stdout instead of the default stderr
    sh = logging.StreamHandler(sys.stdout)

    logger.addHandler(sh)

    return logger


def get_logger():
    return logging.getLogger("klm_homework")