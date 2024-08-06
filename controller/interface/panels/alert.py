import logging

from . import Panel, Rect
from .util import draw_frame
from .text import fitText


from controller.logging import alerts
from controller import term

logger = logging.getLogger(__name__)


class AlertPanel(Panel):
    def __init__(self, transform: Rect):
        super().__init__(transform)
        self.__last_alert = None if len(alerts) == 0 else alerts[-1]

    def should_rerender(self) -> bool:
        changed = len(alerts) > 0 and self.__last_alert != alerts[-1]
        if changed:
            self.__last_alert = alerts[-1]
        return changed

    def render(self):
        # draw frame
        draw_frame(self.transform, "Alerts")

        for i in range(min(len(alerts), self.transform.height - 2)):
            t = fitText(
                str(alerts[-1]),
                Rect(0, 0, self.transform.width - 2, 1),
                parse_special=False,
                wrap=False,
            )[0]
            term.print_raw(
                t,
            )
