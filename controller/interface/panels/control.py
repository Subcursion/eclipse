from . import Panel
from controller.types import Rect
from controller import term
from controller.term import color


class _Control(Panel):
    def __init__(self, transform: Rect, label: str):
        super().__init__(transform)
        self.label = label

    def render(self):
        pass


class IPControl(_Control):
    def __init__(self, transform: Rect):
        super().__init__(transform)


class NumericControl(_Control):
    def __init__(self, transform: Rect):
        super().__init__(transform)
