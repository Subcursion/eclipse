import logging

from .. import Pane
from controller.interface import interface
from controller import term
from controller.types import AnchoredRect
from controller.interface.panels.text import LabelPanel, TextAlignment
from controller.interface.panels.options import OptionsPanel
from controller.interface.panels.alert import AlertPanel
from controller.interface.panels.background import BackgroundPanel

from .connections import ConnectionsPane

logger = logging.getLogger(__name__)


class MainMenu(Pane):
    def __init__(self):
        super().__init__()
        self.art = """
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

        self.__opts_rect = AnchoredRect(
            x=0,
            y=0,
            width=1 / 3 if interface.size[1] > 100 else 1 / 2,
            height=1,
            offset_y=1,
            offset_height=-1,
        )
        self.__alerts_rect = AnchoredRect(
            x=2 / 3 if interface.size[1] > 100 else 1 / 2,
            y=0,
            width=1 / 3 if interface.size[1] > 100 else 1 / 2,
            height=1,
            offset_y=1,
            offset_height=-1,
        )
        self.__art_panel = LabelPanel(
            AnchoredRect(
                1 / 3 + (1 / 6),
                0,
                1 / 3,
                1,
                offset_x=-8,
                offset_y=1,
                offset_height=-1,
            ),
            self.art,
            wrap=False,
            line_stripping=False,
            vertical_alignment=TextAlignment.Start,
            horizontal_alignemnt=TextAlignment.Start,
        )
        self.add_panel(
            LabelPanel(
                AnchoredRect(0, 0, 1, 0, offset_height=1),
                "Welcome to ECLIPSE",
            )
        )

        if interface.size[1] > 100:
            self.add_panel(__art_panel)

        self.add_panel(
            OptionsPanel(
                self.__opts_rect,
                [
                    ("Agent Builder", lambda: None),
                    ("Connections", lambda: interface.push_pane(ConnectionsPane())),
                    ("Settings", lambda: None),
                    ("Quit", lambda: interface.stop_rendering()),
                ],
            )
        )

        self.add_panel(AlertPanel(self.__alerts_rect))

        def resize_listener(size: tuple[int, int]):
            if size[1] < 100:
                self.remove_panel(self.__art_panel)
            else:
                self.add_panel(self.__art_panel)

            if interface.size[1] > 100:
                self.__opts_rect._width = 1 / 3
                self.__alerts_rect._x = 2 / 3
                self.__alerts_rect._width = 1 / 3
            else:
                self.__opts_rect._width = 1 / 2
                self.__alerts_rect._x = 1 / 2
                self.__alerts_rect._width = 1 / 2

        term.add_resize_listener(resize_listener)
