from .. import term
from ..term import input

__size = (0, 0)


def __resize_handler(size: tuple[int, int]):
    global __size
    __size = size


def show_interface():
    # register resize listener
    global __size
    __size = term.get_terminal_size()
    term.add_resize_listener(__resize_handler)

    while True:
        __redraw()
        try:
            input.getch()
        except KeyboardInterrupt:
            term.erase_display(term.EraseMode.All)
            term.use_alternate_screen_buffer(False)
            break


def __redraw():
    # make sure we are on alternate buffer and clear the screen
    term.use_alternate_screen_buffer(True)
    term.set_cursor_visible(False)
    term.erase_display(term.EraseMode.All)

    title = "Welcome to ECLIPSE"
    start_pos = (__size[1] // 2) - (len(title) // 2)
    term.set_cursor_position(col=start_pos)
    term.print_raw("Welcome to ECLIPSE")
    term.set_cursor_position()
