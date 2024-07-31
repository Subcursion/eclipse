from enum import Flag, auto

import controller.term as term
from controller.term.input import InputListener
from controller.types import Rect


import logging

logger = logging.getLogger(__name__)


class VisibilityRules:
    Optional = (auto(),)
    Required = (auto(),)


class Renderable:
    def render(self):
        pass

    def should_rerender(self) -> bool:
        return False

    def cleanup(self) -> None:
        pass


class Panel(Renderable, InputListener):

    def __init__(self, transform: Rect):
        self.transform = transform

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
            term.set_cursor_position(panel.transform.y, panel.transform.x)
            panel.render()

    def input_event(self, input):
        for panel in self.__panels:
            panel.input_event(input)
