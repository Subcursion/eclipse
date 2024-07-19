from typing import Callable

from .base import BaseComponent


class OptionList(BaseComponent):
    def __init__(self, options: list[str], option_selected: Callable[[int], None]):
        if not isinstance(options, list):
            raise ValueError("Option list need to be a list of strings.")

        self.options = options
        self.select = 0
        self.option_selected = option_selected

    def render(self):
        pass
