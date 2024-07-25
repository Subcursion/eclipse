from typing import Callable
import string

from ... import term
from ...term import color
from ...term.style import Style
from ...logging import elog


def DrawOptionList(
    options: list[tuple[str, Callable[[], None]]],
    wrap: bool = True,
    max_items: int = None,
):
    if not isinstance(max_items, int) or max_items < 0:
        raise ValueError("max_items should be 0 for no limit or a positive integer")

    term.set_cursor_visible(False)

    # need to know how much space we have
    ws_cols, ws_rows = term.get_terminal_size()
    cur_col, cur_row = term.get_cursor_position()

    rows_avail = ws_rows - cur_row + 1
    # figure out if we would need to scroll
    if len(options) > rows_avail:
        # see if we have enough to scroll
        pass

    i = 0
    # listen for up down keys
    while True:
        # renderer
        term.save_cursor_position()

        for ind, opt in enumerate(options):
            term.print_raw(
                (
                    color.sgr(
                        Style.BOLD, color.Color_4Bit.BG_CYAN, color.Color_4Bit.FG_BLACK
                    )
                    if i == ind
                    else ""
                ),
                opt[0],
                color.sgr(color.reset()),
            )
            term.move_cursor(term.CursorDirection.Down)
            term.set_cursor_column()
        term.restore_cursor_position()

        # input loop
        c = term.getch()

        if c == "\x0a":
            return options[i][1]()

        if c != term.ESCAPE:
            continue
        c = term.getch()
        if c != "[":
            continue
        n = term.getch()
        if n in string.digits:
            while c in string.digits:
                c = term.getch()
                n += c
            n = int(n)
            direction = c
        elif n in string.ascii_uppercase:
            direction = n
            n = 1
        else:
            continue
        if direction not in "AB":
            continue

        if direction == "B":
            n = -1

        if wrap:
            i = (i - n) % len(options)
        else:
            i -= n
            i = max(0, min(len(options) - 1, i))
