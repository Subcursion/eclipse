from . import Panel

from .. import interface


class LabelPanel(Panel):
    def __init__(
        self,
        transform: Rect,
        content: str,
        fontColor: color.Color_4Bit | tuple[int, int, int] = color.Color_4Bit.FG_WHITE,
    ):
        super().__init__(transform)
        self.content = content
        self.fontColor = fontColor
        self.last_render = datetime.now()

    def should_rerender(self) -> bool:
        return (datetime.now() - self.last_render) > timedelta(seconds=3)

    def input_event(self, content: str):
        if content == " ":
            interface.render_event.set()

    def render(self):
        # determine how many characters we can print
        char_len = min(len(self.content), self.transform.width)
        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print_raw(
            color.sgr(color.fg_color(*c)),
            self.content,
            color.sgr(color.reset()),
        )
        self.last_render = datetime.now()
