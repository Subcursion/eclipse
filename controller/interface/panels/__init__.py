from enum import Flag, auto
import logging

from controller import term
from controller.term.input import InputListener
from controller.types import Rect


logger = logging.getLogger(__name__)


class Renderable:
    def render(self):
        pass

    def should_rerender(self) -> bool:
        return False

    def cleanup(self) -> None:
        pass


class Panel(Renderable, InputListener):

    def __init__(self, transform: Rect, clear: bool = True):
        self.transform = transform
        self.clear = clear

    def render(self):
        pass

    def input_event(self, input):
        pass


class Pane(Renderable, InputListener):

    def __init__(self):
        self.__panels: list[Panel] = []

    def add_panel(self, panel: Panel):
        if panel in self.__panels:
            return
        self.__panels.append(panel)

    def remove_panel(self, panel: Panel):
        if panel not in self.__panels:
            return
        self.__panels.remove(panel)

    def should_rerender(self) -> bool:
        for panel in self.__panels:
            if panel.should_rerender():
                return True
        return False

    def render(self):
        for panel in self.__panels:
            term.set_cursor_position(panel.transform.y, panel.transform.x)
            if panel.clear:
                for y in range(panel.transform.height):
                    term.print_raw(" " * panel.transform.width)
                    term.move_cursor(term.CursorDirection.Down)
                    term.set_cursor_column(panel.transform.x)
                term.set_cursor_position(panel.transform.y, panel.transform.x)
            panel.render()

    def input_event(self, input):
        for panel in self.__panels:
            panel.input_event(input)
