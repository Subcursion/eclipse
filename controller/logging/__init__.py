import logging
import logging.config
from datetime import datetime

__debug_fmt = (
    "%(levelname)s|%(threadName)s@%(asctime)s|"
    + "%(pathname)s:%(lineno)s|%(funcName)s:%(message)s"
)
__norm_fmt = "%(levelname)s|%(asctime)s:%(message)s"

logging_config = {
    "version": 1,
    "formatters": {
        "debug": {
            "format": "%(levelname)s|%(threadName)s@%(asctime)s|"
            + "%(pathname)s:%(lineno)s|%(funcName)s:%(message)s"
        },
        "shortened": {"format": "%(levelname)s|%(asctime)s:%(message)s"},
    },
    "handlers": {
        "default": {
            "class": "logging.NullHandler",
            "level": logging.DEBUG,
            "formatter": "debug",
        }
    },
    "root": {"level": logging.DEBUG, "handlers": ["default"]},
}


class Alert:
    def __init__(self, msg: str):
        self.message = msg
        self.time = datetime.now()

    def __str__(self):
        return f'{self.time.strftime('%H:%M:%S')}:{self.message}'

alerts: list[Alert] = []


def alert(msg: str) -> Alert:
    a = Alert(msg)
    alerts.append(a)
    return a
