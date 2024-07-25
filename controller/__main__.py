import logging

from .interface import interface
from .term.input import input_thread

# parse env args and command line flags

logger = logging.getLogger(__name__)

# start interface loop
try:
    input_thread.start()
    interface.setup_screen()
    interface.render()
except Exception as e:
    logger.error("There was an error during runtime", exc_info=e, stack_info=True)
except KeyboardInterrupt:
    logger.error("Received SIGTERM")
finally:
    input_thread.stop()
    interface.restore_screen()
