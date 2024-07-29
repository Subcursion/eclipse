import enum
import random
import string
from datetime import datetime, timedelta

import controller.term as term
import controller.term.color as color
from controller.types import Rect

from .. import interface
from . import Panel


def fitText(text: str, rect: Rect) -> list[str]:
    # first, if wrap is enabled, split content up to fit each line until we are out of content
    # or space
    start_index = 0
    end_index = min(len(text), rect.width)
    lines = []

    if end_index == len(text):
        lines.append(text)  # all fits on single line
    else:
        while len(lines) < rect.height:
            c = text[end_index - 1]
            while c not in string.whitespace:
                end_index -= 1
                c = text[end_index - 1]

            if len(lines) == rect.height - 1:
                # make room for ellipsis
                left = min(3, rect.width - (end_index - start_index))

            lines.append(text[start_index:end_index].strip())

            start_index = end_index + 1
            end_index = start_index + min(len(text) - start_index, rect.width)
            if end_index == len(text):
                break


class TextAlignment(enum.IntEnum):
    Start = enum.auto()
    Middle = enum.auto()
    End = enum.auto()


class LabelPanel(Panel):
    def __init__(
        self,
        transform: Rect,
        content: str,
        fontColor: color.Color_4Bit | tuple[int, int, int] = color.Color_4Bit.FG_WHITE,
        horizontal_alignemnt: TextAlignment = TextAlignment.Middle,
        vertical_alignment: TextAlignment = TextAlignment.Middle,
        wrap: bool = True,
    ):
        super().__init__(transform)
        self.content = content
        self.fontColor = fontColor
        self.last_render = datetime.now()
        self.horizontal_alignemnt = horizontal_alignemnt
        self.vertical_alignment = vertical_alignment
        self.wrap = wrap

    def __randomize_color(self):
        self.fontColor = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def should_rerender(self) -> bool:
        val = (datetime.now() - self.last_render) > timedelta(seconds=3)
        if val:
            self.__randomize_color()
        return val

    def input_event(self, content: str):
        if content == " ":
            self.__randomize_color()
            interface.render_event.set()

    def render(self):

        char_len = min(len(self.content), self.transform.width)
        term.print_raw(
            color.sgr(
                color.fg_4bit(self.fontColor)
                if isinstance(self.fontColor, color.Color_4Bit)
                else color.fg_color(*self.fontColor)
            ),
            self.content[: char_len + 1],
            color.sgr(color.reset()),
        )
        self.last_render = datetime.now()
