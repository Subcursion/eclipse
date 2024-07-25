from traceback import format_exc

import logging

from . import term
from .interface import interface
from .term.input import input_thread
from .logging import setup_loggers

# parse env args and command line flags

setup_loggers()
logger = logging.getLogger(__name__)

# start interface loop
try:
    input_thread.start()
    interface.setup_screen()
    interface.render()
except Exception as e:
    logger.error("There was an error during runtime", exc_info=e, stack_info=True)
except KeyboardInterrupt:
    logging.error("Received SIGTERM")
finally:
    input_thread.stop()
    interface.restore_screen()
