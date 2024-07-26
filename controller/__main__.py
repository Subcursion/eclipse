import logging
import logging.config
import argparse
import os


from .logging import logging_config

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# don't import local packages until logging has been configured
from .interface import interface
from .term.input import input_thread
from .term.color import Color_4Bit

from .interface.components import LabelPanel, Rect

# parse command line args


# parse environment args (override method)
log_file = os.getenv("LOGFILE", None)
if log_file is not None:
    logging.getLogger("root").addHandler(logging.FileHandler(log_file, mode="w+"))

# start interface loop
try:
    input_thread.start()
    interface.setup_screen()

    main_menu = interface.push_pane()
    main_menu.add_panel(
        LabelPanel(Rect(1, 1, 30, 30), "Welcome to ECLIPSE", Color_4Bit.FG_BLUE)
    )

    interface.render()
except Exception as e:
    logger.error("There was an error during runtime", exc_info=e)
except KeyboardInterrupt:
    logger.error("Received SIGTERM")
finally:
    input_thread.stop()
    interface.restore_screen()
