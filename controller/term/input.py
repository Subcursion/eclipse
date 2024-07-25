import sys
import threading
import string
from typing import Callable
import termios

from .. import term
from ..logging import elog


class __InputThread(threading.Thread):

    def __init__(self):
        super().__init__(name="ECLInputT", daemon=True)
        self.quit_event = threading.Event()

        try:
            import msvcrt

            self.getch = msvcrt.getch
            self.__og_tcs = None
        except ImportError:
            import tty

            self.__og_tcs = tty.setcbreak(sys.stdin.fileno(), when=termios.TCSANOW)
            self.getch = lambda: sys.stdin.read(1)

    def run(self):
        from ..interface import interface

        c = None
        while not self.quit_event.is_set():
            c = self.getch()
            if c == term.ESCAPE:
                # read bracket
                b = self.getch()
                if b != "[":
                    pass
                # read until a capital letter
                c = self.getch()
                var = ""
                while c not in string.ascii_uppercase:
                    var += c
                    c = self.getch()
                var = var.split(";")
            else:
                interface.input_event(c)
        elog("Exited input loop")

    def stop(self):
        elog("Stopping input thread")
        self.quit_event.set()
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.__og_tcs)


input_thread = __InputThread()


class InputListener:
    def input_event(self, input: str):
        pass
