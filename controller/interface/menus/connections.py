import logging

from controller.interface import Pane, interface
from controller.interface.panels import Panel
from controller.interface.panels.background import BackgroundPanel
from controller.interface.panels.options import OptionsPanel
from controller.types import AnchoredRect, Rect
from controller.interface.panels.util import draw_frame
from controller import term


logger = logging.getLogger(__name__)


class _IPModial(Panel):
    def __init__(self, transform: Rect):
        super().__init__(transform)

    def input_event(self, input):
        if input == term.BACKSPACE or input == term.ESCAPE:
            interface.pop_pane()
            interface.request_rerender()

    def render(self):
        draw_frame(self.transform, "Enter IPv4 & Port")


class ConnectionsPane(Pane):
    def __init__(self):
        super().__init__()

        self.__opt_panel = OptionsPanel(
            AnchoredRect(0, 0, 1, 1, offset_y=1, offset_height=-1),
            options=[
                ("Create Listener", lambda: None),
                ("Connecto to Agent", lambda: self.show_connection_modial()),
                ("Main Menu", lambda: interface.pop_pane()),
            ],
        )
        self.add_panel(self.__opt_panel)

    def input_event(self, input):
        super().input_event(input)
        if input == term.BACKSPACE:
            interface.pop_pane()

    def show_connection_modial(self):
        mod_pane = interface.push_pane()
        mod_pane.add_panel(
            _IPModial(AnchoredRect(0.25, 0.5, 0.5, 0, offset_y=-3, offset_height=7))
        )
