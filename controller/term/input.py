from typing import Callable

__input_listeners: list[Callable[[str], None]] = []


def add_input_listener(listener: Callable[[str], None]):
    if listener in __input_listeners:
        __input_listeners.add(listener)


def remove_input_listener(listener: Callable[[str], None]):
    if listener in __input_listeners:
        __input_listeners.remove(listener)


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
        pass

    def __call__(self):
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(sys.stdin.fileno(), when=termios.TCSAFLUSH)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _Getch()
