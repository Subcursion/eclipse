import random

from .. import term
from ..logging import elog
from ..term import input
from ..term.color import fg_color, reset, sgr

from .components.options import DrawOptionList

__size = (0, 0)


def __resize_handler(size: tuple[int, int]):
    global __size
    elog("Resize handler called, old", __size, "new", size)
    __size = size
    __redraw()


def show_interface():
    # initial setup
    term.use_alternate_screen_buffer(True)
    # term.set_cursor_visible(False)
    term.erase_display(term.EraseMode.All)

    # register resize listener
    global __size
    __size = term.get_terminal_size()
    elog("Initial size", __size)
    term.add_resize_listener(__resize_handler)

    while True:
        __redraw()


def close_interface():
    term.erase_display(term.EraseMode.All)
    term.use_alternate_screen_buffer(False)
    exit(0)


def __redraw():
    # make sure we are on alternate buffer and clear the screen
    term.use_alternate_screen_buffer(True)
    term.set_cursor_visible(False)
    term.erase_display(term.EraseMode.All)

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    title = "Welcome to ECLIPSE"
    start_pos = (__size[1] // 2) - (len(title) // 2)
    term.set_cursor_position(row=1, col=start_pos)
    term.print_raw(sgr(fg_color(*color)), title, sgr(reset()))

    term.move_cursor(term.CursorDirection.Down, 2)
    term.set_cursor_column()

    DrawOptionList(
        [
            ("Agent Management", lambda: elog("First option selected")),
            ("Listeners", lambda: elog("Second option selected")),
            ("Settings", lambda: elog("Third option selected")),
            ("Agent Management", lambda: elog("First option selected")),
            ("Listeners", lambda: elog("Second option selected")),
            ("Settings", lambda: elog("Third option selected")),
            ("Quit", close_interface),
        ],
        wrap=False,
    )
