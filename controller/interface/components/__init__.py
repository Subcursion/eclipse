from typing import Callable


class Renderable:
    def render(self):
        pass


class Panel(Renderable):

    def __init__(self):
        pass

    def render(self):
        pass


class Pane(Renderable):

    def __init__(self):
        self.__panels = []

    def add_panel(self, panel: Panel):
        self.__panels.append(panel)

    def remove_panel(self, panel: Panel):
        self.__panels.remove(panel)

    def render(self):
        for panel in self.__panels:
            panel.render()


class OptionPanel(Panel):

    def __init__(self, options: list[tuple[str, Callable[[], None]]]):
        super().__init__()
        self.__options = options
