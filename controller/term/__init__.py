import signal
import typing

from ..types import ANSI_Enum
from .input import getch

ESCAPE = chr(0x1B)
CSI = ESCAPE + "["

ARG_SEP = ";"

__resize_listeners: list[typing.Callable[[int, int], None]] = []

__old_handler = None


def __update_term_size(signum, frame):
    if __old_handler:
        __old_handler(signum, frame)
    size = get_terminal_size()
    for listener in __resize_listeners:
        listener(size)


__old_handler = signal.signal(signal.SIGWINCH, __update_term_size)


def print_raw(
    *values: object,
    sep: str | None = "",
    end: str | None = "",
    flush: typing.Literal[False] = True
) -> None:
    print(*values, sep=sep, end=end, flush=flush)


def add_resize_listener(listener: callable):
    if listener not in __resize_listeners:
        __resize_listeners.append(listener)


def remove_resize_listener(listener: callable):
    if listener in __resize_listeners:
        __resize_listeners.remove(listener)


def use_alternate_screen_buffer(use: bool = True):
    print_raw(CSI + "?1049" + ("h" if use else "l"))


class CursorDirection(ANSI_Enum):
    Up = "A"
    Down = "B"
    Forward = "C"
    Back = "D"
    NextLine = "E"
    PrevLine = "F"
    HorizontalAbs = "G"


def move_cursor(direction: CursorDirection, n: int = 1):
    print_raw(CSI + str(n) + direction)


def set_cursor_position(row: int = 1, col: int = 1):
    print_raw(CSI + str(row) + ARG_SEP + str(col) + "H")


def get_cursor_position() -> tuple[int, int]:
    from ..logging import log_to_main_term

    print_raw(CSI + "6n")

    esc = getch()
    if esc != ESCAPE:
        log_to_main_term("Expected escape return code, got", ord(esc), esc)
        return (-1, -1)
    bracket = getch()
    if bracket != "[":
        log_to_main_term("Expected bracket return code, got", ord(bracket), bracket)
        return (-1, -1)

    n = getch()
    curr = getch()
    while curr != ";":
        n += curr
        curr = getch()

    m = getch()
    curr = getch()
    while curr != "R":
        m += curr
        curr = getch()

    return (int(n), int(m))


def get_terminal_size() -> tuple[int, int]:
    save_cursor_position()
    set_cursor_position(9999, 9999)
    h, w = get_cursor_position()
    restore_cursor_position()
    return (h, w)


class EraseMode(ANSI_Enum):
    PosToEnd = "0"
    PosToBegin = "1"
    All = "2"
    History = "3"


def erase_display(mode: EraseMode):
    print_raw(CSI + mode + "J")


def erase_line(mode: EraseMode):
    if mode == EraseMode.History:
        raise NotImplementedError(
            EraseMode.History + " is not implemented for line erasing."
        )
    print_raw(CSI + mode + "K")


def scroll(n: int = 1):
    print_raw(CSI + str(n) + ("S" if n > 0 else "T"))


def set_cursor_visible(visible: bool):
    print_raw(CSI + "?25" + ("h" if visible else "l"))


def save_cursor_position():
    print_raw(CSI + "s")


def restore_cursor_position():
    print_raw(CSI + "u")
