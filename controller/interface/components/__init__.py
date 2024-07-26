from typing import Callable
import threading
from datetime import timedelta, datetime
import random

from ...term.input import InputListener
from ...term import print_raw
from ...term import color, set_cursor_position
from ...term.style import Style

from ..structs import Rect


class Renderable:
    def render(self):
        pass

    def should_rerender(self) -> bool:
        return False


class Panel(Renderable, InputListener):

    def __init__(self, transform: Rect):
        self.transform = transform

    def check_for_render(self):
        pass

    def render(self):
        pass

    def input_event(self, input):
        pass


class Pane(Renderable, InputListener):

    def __init__(self):
        self.__panels: list[Panel] = []

    def add_panel(self, panel: Panel):
        self.__panels.append(panel)

    def remove_panel(self, panel: Panel):
        self.__panels.remove(panel)

    def should_rerender(self) -> bool:
        for panel in self.__panels:
            if panel.should_rerender():
                return True
        return False

    def render(self):
        for panel in self.__panels:
            set_cursor_position(panel.transform.x, panel.transform.y)
            panel.render()

    def input_event(self, input):
        for panel in self.__panels:
            panel.input_event(input)
