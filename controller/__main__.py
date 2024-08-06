import logging
import logging.config
import os

from .logging import logging_config

log_file = os.getenv("LOGFILE", None)
if log_file is not None:
    handler = logging_config["handlers"]["default"]
    handler["class"] = "logging.FileHandler"
    handler["filename"] = log_file
    handler["mode"] = "w+"
    logging_config["handlers"]["default"] = handler

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    from .interface import interface
    from .term.input import input_thread
    from . import term
    from .interface.menus.main import MainMenu

    # start interface loop
    try:
        logger.debug("Starting input thread")
        input_thread.start()
        logger.debug("Initializing screen")
        interface.setup_screen()

        interface.push_pane(MainMenu())

        logger.debug("Starting render")
        interface.render()
    except Exception as e:
        logger.error("There was an error during runtime", exc_info=e)
    except KeyboardInterrupt:
        logger.debug("Received SIGTERM")
    finally:
        input_thread.stop()
        interface.restore_screen()
