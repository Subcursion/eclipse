import enum
import random
import string
from datetime import datetime, timedelta
import re
import logging

import controller.term as term
import controller.term.color as color
from controller.types import Rect

from .. import interface
from . import Panel

logger = logging.getLogger(__name__)


def escape(text: str):
    text = re.sub(r"\n", "\\n", text)
    text = re.sub(r"\t", "\\t", text)
    return text


def fitText(
    text: str,
    rect: Rect,
    parse_special: bool = True,
    wrap: bool = True,
    line_stripping: bool = True,
    overflow_ellipsis: bool = True,
) -> list[str]:
    # convert tabs to 4 full spaces
    if line_stripping:
        text = text.strip()
    pre_lines = []
    if parse_special:
        text = re.sub(r"\t", "    ", text)
        # convert new lines to seperate lines
        pre_lines = text.split("\n")
    else:
        pre_lines = [escape(text)]

    lines = []
    # for each line, see if it would fit
    if wrap:
        for line_i, line in enumerate(pre_lines):
            if line_stripping:
                line = line.strip()
            if len(line) < rect.width:
                lines.append(line)
                continue

            # go back until a whitespace is found we can break on
            i = rect.width
            # edge case: we landed on a character but the next character is whitespace
            # we are already guaranteed to have at least one more character available
            if line[i] in string.whitespace:
                lines.append(line[:i])
                while i < len(line) and line[i] in string.whitespace:
                    i += 1
                pre_lines.insert(line_i + 1, line[i:])
                continue
            # can't fit line, move cursor back until we find whitespace
            while i >= 0 and line[i] not in string.whitespace:
                i -= 1

            if i == -1:
                # no breakable characters, just add what we can as a line
                lines.append(line[: rect.width])
                pre_lines.insert(line_i + 1, line[rect.width :])
                continue
            lines.append(line[:i])
            # move i forward until none whitespace
            while i < len(line) and line[i] in string.whitespace:
                i += 1
            pre_lines.insert(line_i + 1, line[i:])

    else:
        lines = pre_lines

    # for any lines that are longer than the available space, truncate.
    # or if it's the last line and there is more lines, truncate appropiate
    for line_i, line in enumerate(lines):
        if line_i > rect.height:
            break
        if len(line) > rect.width or (
            line_i == rect.height - 1 and len(lines) > rect.height
        ):
            if overflow_ellipsis:
                lines[line_i] = line[: min(len(line), rect.width - 3)] + "..."
            else:
                lines[line_i] = line[: rect.width]
    lines = lines[: rect.height]

    return lines


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
        line_stripping: bool = True,
    ):
        super().__init__(transform)
        self.content = content
        self.fontColor = fontColor
        self.horizontal_alignemnt = horizontal_alignemnt
        self.vertical_alignment = vertical_alignment
        self.wrap = wrap
        self.line_stripping = line_stripping

    def __randomize_color(self):
        self.fontColor = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def render(self):

        # term.save_cursor_position()
        # for i in range(self.transform.height):
        #     term.set_cursor_column(self.transform.x)
        #     term.print_raw(
        #         color.sgr(color.color_4bit(color.Color_4Bit.BG_BLUE)),
        #         " " * self.transform.width,
        #         color.sgr(color.reset()),
        #     )
        #     term.move_cursor(term.CursorDirection.Down)

        # term.restore_cursor_position()

        lines = fitText(
            self.content,
            self.transform,
            wrap=self.wrap,
            line_stripping=self.line_stripping,
        )
        # figure out which vertical row should start on
        if self.vertical_alignment == TextAlignment.Middle:
            term.move_cursor(
                term.CursorDirection.Down,
                (self.transform.height // 2) - (len(lines) // 2),
            )
        elif self.vertical_alignment == TextAlignment.End:
            term.move_cursor(
                term.CursorDirection.Down, self.transform.height - len(lines)
            )

        # per row horixontal alignment
        for line in lines:
            term.set_cursor_column(self.transform.x)
            if self.horizontal_alignemnt == TextAlignment.Middle:
                term.move_cursor(
                    term.CursorDirection.Forward,
                    (self.transform.width // 2) - (len(line) // 2),
                )
            elif self.horizontal_alignemnt == TextAlignment.End:
                term.move_cursor(
                    term.CursorDirection.Forward, self.transform.width - len(line)
                )
            term.print_raw(
                # color.sgr(color.color_4bit(color.Color_4Bit.BG_GREEN)),
                color.sgr(
                    color.color_4bit(self.fontColor)
                    if isinstance(self.fontColor, color.Color_4Bit)
                    else color.fg_color(*self.fontColor)
                ),
                line,
                color.sgr(color.reset()),
            )
            term.move_cursor(term.CursorDirection.Down)
