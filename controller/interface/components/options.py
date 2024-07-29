import string
from typing import Callable

import controller.term as term
import controller.term.color as color
from controller.term.style import Style
from controller.types import Rect
from controller.interface.components import Panel
from controller.interface import interface


class OptionsPanel(Panel):

    def __init__(
        self,
        transform: Rect,
        options: list[tuple[str, Callable[[], None]]],
        wrap: bool = False,
    ):
        super().__init__(transform)
        self.options = options
        if len(options) == 0:
            raise ValueError("At least one option must be specified")
        self.selected = 0
        self.wrap = wrap

    def input_event(self, input: str):
        if input == term.UP_ARROW:
            self.selected -= 1
        elif input == term.DOWN_ARROW:
            self.selected += 1
        elif input == term.ENTER:
            self.options[self.selected][1]()
        else:
            return

        if self.wrap:
            self.selected = self.selected % len(self.options)
        else:
            self.selected = min(len(self.options) - 1, max(0, self.selected))
        interface.request_rerender()

    def render(self):
        for opt_i, opt in enumerate(self.options):
            term.set_cursor_column(self.transform.x)
            term.print_raw(
                (
                    ""
                    if self.selected != opt_i
                    else color.sgr(
                        Style.BOLD,
                        color.set_color(fg=(0, 0, 0), bg=(50, 100, 150)),
                    )
                ),
                opt[0] + (" " * (self.transform.width - len(opt[0]))),
                color.sgr(color.reset()),
            )
            term.move_cursor(term.CursorDirection.Down)
