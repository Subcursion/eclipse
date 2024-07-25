import sys
import logging


class EclipseFormatter(logging.Formatter):

    __debug_fmt = "%(levelname)s|%(threadName)s@%(asctime)s|%(pathname)s:%(lineno)s|%(funcName)s:%(message)s"
    __norm_fmt = "%(levelname)s|%(asctime)s:%(message)s"

    def __init__(self):
        super().__init__(
            fmt="%(levelname)s|%(name)s@%(asctime)s: %(message)s",
            datefmt=None,
            style="%",
        )

    def format(self, record):
        pass


def setup_loggers():
    # since we are taking control of the terminal, we can't output there.
    # by default, we will output to a file without color
    logging.basicConfig(
        filename=".log", filemode="w+", format=basic_format, level=logging.DEBUG
    )


def elog(*args, **kargs):
    file = kargs.pop("file", sys.stderr)
    print(*args, **kargs, file=file)
