from enum import StrEnum
import logging

logger = logging.getLogger(__name__)


class ANSI_Enum(StrEnum):
    def __str__(self):
        return self.value

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)


class Rect:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width - 1

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height - 1

    def include(self, other: "Rect"):
        r = max(self.right, other.right)
        b = max(self.bottom, other.bottom)
        self.x = max(min(self.x, other.x), 1)
        self.y = max(min(self.y, other.y), 1)
        self.width = r - self.x
        self.height = b - self.y


class AnchoredRect(Rect):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        offset_x: int = 0,
        offset_y: int = 0,
        offset_width: int = 0,
        offset_height: int = 0,
    ):
        from controller.interface import interface

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._interface = interface
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_width = offset_width
        self.offset_height = offset_height

    @property
    def x(self):
        logger.debug("Referencing x")
        return round((self._interface.size[1] - 1) * self._x) + 1 + self.offset_x

    @property
    def y(self):
        logger.debug("Referencing y")
        return round((self._interface.size[0] - 1) * self._y) + 1 + self.offset_y

    @property
    def width(self):
        logger.debug("Referencing width")
        return int((self._interface.size[1]) * self._width) + self.offset_width

    @property
    def height(self):
        logger.debug("Referencing height")
        return int((self._interface.size[0]) * self._height) + self.offset_height
