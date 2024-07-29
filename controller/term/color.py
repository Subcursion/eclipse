import logging

from ..types import ANSI_Enum
from . import ARG_SEP, CSI
from .style import Style

logger = logging.getLogger(__name__)

BIT_8 = "5"
BIT_24 = "2"
FG_8BIT = "38"
BG_8BIT = "48"
UNDERLINE_8BIT = "58"


class Color_4Bit(ANSI_Enum):
    FG_BLACK = "30"
    FG_RED = "31"
    FG_GREEN = "32"
    FG_YELLOW = "33"
    FG_BLUE = "34"
    FG_MAGENTA = "35"
    FG_CYAN = "36"
    FG_WHITE = "37"
    FG_DEFAULT = "39"

    BG_BLACK = "40"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_MAGENTA = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"
    BG_DEFAULT = "49"

    FG_BRIGHT_BLACK = "90"
    FG_BRIGHT_RED = "91"
    FG_BRIGHT_GREEN = "92"
    FG_BRIGHT_YELLOW = "93"
    FG_BRIGHT_BLUE = "94"
    FG_BRIGHT_MAGENTA = "95"
    FG_BRIGHT_CYAN = "96"
    FG_BRIGHT_WHITE = "97"

    BG_BRIGHT_BLACK = "100"
    BG_BRIGHT_RED = "101"
    BG_BRIGHT_GREEN = "102"
    BG_BRIGHT_YELLOW = "103"
    BG_BRIGHT_BLUE = "104"
    BG_BRIGHT_MAGENTA = "105"
    BG_BRIGHT_CYAN = "106"
    BG_BRIGHT_WHITE = "107"


UNDERLINE_DEFAULT = "59"


def sgr(*n: str | Color_4Bit | Style | list[str | Color_4Bit | Style]) -> str:
    res = (
        CSI
        + ARG_SEP.join(
            [
                str(m) if (isinstance(m, (str, Color_4Bit, Style))) else m.join(ARG_SEP)
                for m in n
            ]
        )
        + "m"
    )
    # logger.debug("SGR: %s", res.encode(), stack_info=True)
    return res


def reset() -> str:
    return str(Style.RESET)


def color_4bit(*args: Color_4Bit) -> str:
    return ARG_SEP.join(args)


def fg_8bit(n) -> str:
    return FG_8BIT + ARG_SEP + BIT_8 + ARG_SEP + str(n)


def bg_8bit(n) -> str:
    return BG_8BIT + ARG_SEP + BIT_8 + ARG_SEP + str(n)


def underline_8bit(n) -> str:
    return UNDERLINE_8BIT + ARG_SEP + BIT_8 + ARG_SEP + str(n)


def color_8bit(fgn, bgn) -> str:
    return fg_8bit(fgn) + ARG_SEP + bg_8bit(bgn)


def fg_color(r, g, b) -> str:
    return (
        FG_8BIT
        + ARG_SEP
        + BIT_24
        + ARG_SEP
        + str(r)
        + ARG_SEP
        + str(g)
        + ARG_SEP
        + str(b)
    )


def bg_color(r, g, b) -> str:
    return (
        BG_8BIT
        + ARG_SEP
        + BIT_24
        + ARG_SEP
        + str(r)
        + ARG_SEP
        + str(g)
        + ARG_SEP
        + str(b)
    )


def set_color(fg: tuple[int, int, int], bg: tuple[int, int, int]):
    return fg_color(*fg) + ARG_SEP + bg_color(*bg)


def underline_color(r, g, b) -> str:
    return (
        UNDERLINE_8BIT
        + ARG_SEP
        + BIT_24
        + ARG_SEP
        + str(r)
        + ARG_SEP
        + str(g)
        + ARG_SEP
        + str(b)
    )
