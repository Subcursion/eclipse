import random

from .. import term
from ..logging import elog
from ..term import input
from ..term.color import fg_color, reset, sgr

from .components.options import DrawOptionList
from .components import Pane, Panel, Renderable
from ..term.input import InputListener


class __Interface(Renderable, InputListener):
    def __init__(self):
        self.__panes = []
        self.__size = (0, 0)

        def __resized(size: tuple[int, int]):
            self.__size = size

        term.add_resize_listener(__resized)

    def setup_screen(self):
        elog("Setting up screen")
        term.use_alternate_screen_buffer(True)
        term.erase_display(term.EraseMode.All)
        term.set_cursor_position(1, 1)
        term.set_cursor_visible(False)

    def restore_screen(self):
        elog("Restoring screen")
        term.erase_display(term.EraseMode.All)
        term.use_alternate_screen_buffer(False)
        term.set_cursor_visible(True)

    def push_pane():
        p = Pane()
        __panes.append(p)
        return p

    def pop_pane():
        return __panes.pop()

    def input_event(self, input: str):
        elog("Received input!", input)

    def render(self):
        while True:
            for pane in self.__panes:
                pane.render()


interface = __Interface()
