import sys


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
