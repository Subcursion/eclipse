import logging
import threading
import time

import controller.term as term
from controller.term.input import InputListener

from .panels import Pane, Renderable

logger = logging.getLogger(__name__)


class __Interface(Renderable, InputListener):
    def __init__(self):
        self.__panes: list[Pane] = []
        self.__size = (0, 0)
        self.render_event = threading.Event()
        self.render_event.set()
        self.keep_rendering = True

        def __resized(size: tuple[int, int]):
            self.__size = size
            self.request_rerender()

        term.add_resize_listener(__resized)

    @property
    def size(self):
        return self.__size

    def setup_screen(self):
        term.use_alternate_screen_buffer(True)
        term.erase_display(term.EraseMode.All)
        term.set_cursor_position(1, 1)
        term.set_cursor_visible(False)
        self.__size = term.get_terminal_size()

    def restore_screen(self):
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

    def request_rerender(self) -> None:
        self.render_event.set()

    def stop_rendering(self) -> None:
        self.keep_rendering = False
        # tell all children to clean up
        for pane in self.__panes:
            pane.cleanup()
        self.cleanup()

    def render(self):
        while self.keep_rendering:
            if self.render_event.is_set():
                term.erase_display(term.EraseMode.All)
                for pane in self.__panes:
                    pane.render()
                self.render_event.clear()
            else:
                time.sleep(0.01)  # do this to not hog CPU
                if self.should_rerender():
                    self.render_event.set()


interface = __Interface()
