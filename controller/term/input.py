import logging
import string
import sys
import termios
import threading

from .. import term

logger = logging.getLogger()


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

            self.__og_tcs = termios.tcgetattr(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno(), when=termios.TCSANOW)
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
                interface.input_event(term.ESCAPE + b + var + c)
            else:
                interface.input_event(c)
        logger.error("Exited input loop")

    def stop(self):
        logger.debug("Stopping input thread")
        self.quit_event.set()
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.__og_tcs)


input_thread = __InputThread()


class InputListener:
    def input_event(self, input: str):
        pass
