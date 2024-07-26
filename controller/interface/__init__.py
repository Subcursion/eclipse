import random
import logging
import threading
import time

from .. import term
from ..term import input
from ..term.color import fg_color, reset, sgr

from .components import Pane, Panel, Renderable
from ..term.input import InputListener

logger = logging.getLogger(__name__)


class __Interface(Renderable, InputListener):
    def __init__(self):
        self.__panes: list[Pane] = []
        self.__size = (0, 0)
        self.render_event = threading.Event()
        self.render_event.set()

        def __resized(size: tuple[int, int]):
            self.__size = size

        term.add_resize_listener(__resized)

    @property
    def size(self):
        return self.__size

    def setup_screen(self):
        logger.error("Setting up screen")
        term.use_alternate_screen_buffer(True)
        term.erase_display(term.EraseMode.All)
        term.set_cursor_position(1, 1)
        term.set_cursor_visible(False)

    def restore_screen(self):
        logger.error("Restoring screen")
        term.erase_display(term.EraseMode.All)
        term.use_alternate_screen_buffer(False)
        term.set_cursor_visible(True)

    def push_pane(self) -> Pane:
        p = Pane()
        self.__panes.append(p)
        return p

    def pop_pane(self) -> Pane:
        return self.__panes.pop()

    def input_event(self, input: str):
        if len(self.__panes) == 0:
            return
        # only pass input to top panel
        self.__panes[-1].input_event(input)

    def should_rerender(self) -> bool:
        for pane in self.__panes:
            if pane.should_rerender():
                return True
        return False

    def render(self):
        while True:
            if self.render_event.is_set():
                term.erase_display(term.EraseMode.All)
                for pane in self.__panes:
                    pane.render()
                self.render_event.clear()
            else:
                if self.should_rerender():
                    self.render_event.set()


interface = __Interface()
