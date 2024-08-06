from . import Panel, Rect
from controller.term import color
from controller import term


class BackgroundPanel(Panel):
    def __init__(
        self, transform: Rect, color: color.Color_4Bit | tuple[int, int, int] = None
    ):
        super().__init__(transform)
        self.color = color

    def render(self):
        for y in range(self.transform.height):
            term.set_cursor_column()
            term.print_raw(
                (
                    (
                        color.sgr(color.color_4bit(self.color))
                        if isinstance(self.color, color.Color_4Bit)
                        else color.sgr(color.bg_color(*self.color))
                    )
                    if self.color is not None
                    else ""
                ),
                " " * self.transform.width,
                color.sgr(color.reset()),
            )
            term.move_cursor(term.CursorDirection.Down)
