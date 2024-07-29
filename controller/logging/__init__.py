import logging
import logging.config

__debug_fmt = (
    "%(levelname)s|%(threadName)s@%(asctime)s|"
    + "%(pathname)s:%(lineno)s|%(funcName)s:%(message)s"
)
__norm_fmt = "%(levelname)s|%(asctime)s:%(message)s"

logging_config = {
    "version": 1,
    "handlers": {
        "nooutput": {
            "class": "logging.NullHandler",
            "level": logging.DEBUG,
        }
    },
    "root": {"level": logging.DEBUG, "handlers": ["nooutput"]},
}
