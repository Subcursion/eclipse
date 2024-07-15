from ..types import ANSI_Enum


class Style(ANSI_Enum):
    RESET = "0"
    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    SLOW_BLINK = "5"
    RAPID_BLINK = "6"
    INVERT = "7"
    CONCEAL = "8"
    CROSSOUT = "9"
    PRIMARY_FONT = "10"
    ALTERNATE_FONT = "11"
    GOTHIC = "20"
    NOT_BOLD = "21"
    NORMAL = "22"
    NOT_ITALIC_OR_BLACKLETTER = "23"
    NOT_UNDERLINED = "24"
    NOT_BLINKING = "25"
    PROPORTIONAL_SPACED = "26"
    NOT_REVERSED = "27"
    NOT_CONCEALED = "28"
    NOT_CROSSEDOUT = "29"
    NOT_PROPORTIONAL_SPACED = "50"
    FRAMED = "51"
    ENCIRCLED = "52"
    OVERLINE = "53"
    NOT_FRAMED_OR_ENCIRCLED = "54"
    NOT_OVERLINE = "55"
    RIGHT_SIDE_LINE = "60"
    RIGHT_DOUBLE_LINE = "61"
    LEFT_SIDE_LINE = "62"
    LEFT_DOUBLE_LINE = "63"
    STRESS_MARKING = "64"
    NOT_IDEOGRAM_MARKED = "65"
    SUPERSCRIPT = "73"
    SUBSCRIPT = "74"
    NOT_SUPER_OR_SUB_SCRIPT = "75"

    def __str__(self):
        return self.value

    def __add__(self, other):
        if other is str and other is not Style:
            raise TypeError("Style cannot be combined with a " + type(other))
        return str(self) + str(other)

    def __radd__(self, other):
        if other is str and other is not Style:
            raise TypeError("Style cannot be combined with a " + type(other))
        return str(other) + str(self)
