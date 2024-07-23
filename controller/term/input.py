import sys
import threading
import string
from typing import Callable

from .. import term


class InputThread(threading.Thread):

    def __init__(self):
        super().__init__(name="ECLInputT", daemon=False)

    def run(self):
        c = None
        while True:
            c = getch()
            if c == term.ESCAPE:
                # read bracket
                b = getch()
                if b != "[":
                    pass
                # read until a capital letter
                c = getch()
                var = ""
                while c not in string.ascii_uppercase:
                    var += c
                    c = getch()
                var = var.split(";")


def listen_for(*seq: str | bytes | list[str | bytes]):
    pass


def listen():
    pass


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""

    def __init__(self):
        try:
            import msvcrt

            self.impl = msvcrt.getch
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import termios

        self.old_settings = termios.tcgetattr(sys.stdin.fileno())

    def __call__(self):
        import termios
        import tty

        tty.setcbreak(sys.stdin, when=tty.TCSANOW)
        ch = None
        try:
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.old_settings)
        return ch


getch_raw = _Getch()
getch = _Getch()
