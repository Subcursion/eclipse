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

art = """
 ,_     _
 |\\\\_,-~/
 / _  _ |    ,--.
(  @  @ )   / ,-'
 \\  _T_/-._( (
 /         `. \\
|         _  \\ |
 \\ \\ ,  /      |
  || |-_\\__   /
 ((_/`(____,-'
 """.strip(
    "\n"
)

if __name__ == "__main__":
    from .interface import interface
    from .types import Rect, AnchoredRect
    from .interface.components.text import LabelPanel, TextAlignment
    from .interface.components.options import OptionsPanel
    from .term.input import input_thread

    from .interface.components.text import fitText

    def view_connections():
        logger.debug("Connections would be viewed")

    # start interface loop
    try:
        logger.debug("Starting input thread")
        input_thread.start()
        logger.debug("Initializing screen")
        interface.setup_screen()

        logger.debug("Building main pane")
        main_menu = interface.push_pane()
        main_menu.add_panel(
            LabelPanel(
                AnchoredRect(0, 0, 1, 0, offset_height=1),
                "Welcome to ECLIPSE",
            )
        )
        main_menu.add_panel(
            LabelPanel(
                AnchoredRect(
                    1 / 3 + (1 / 6),
                    0,
                    1 / 3,
                    1,
                    offset_x=-8,
                    offset_y=1,
                    offset_height=-1,
                ),
                art,
                wrap=False,
                line_stripping=False,
                vertical_alignment=TextAlignment.Start,
                horizontal_alignemnt=TextAlignment.Start,
            )
        )
        main_menu.add_panel(
            OptionsPanel(
                AnchoredRect(0, 0, 1 / 3, 1, offset_y=1, offset_height=-1),
                [
                    ("Agent Builder", lambda: None),
                    ("Connections", view_connections),
                    ("Settings", lambda: None),
                    ("Quit", lambda: interface.stop_rendering()),
                ],
            )
        )
        logger.debug("Starting render")
        interface.render()
    except Exception as e:
        logger.error("There was an error during runtime", exc_info=e)
    except KeyboardInterrupt:
        logger.debug("Received SIGTERM")
    finally:
        input_thread.stop()
        interface.restore_screen()
