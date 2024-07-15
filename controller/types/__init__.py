from enum import StrEnum


class ANSI_Enum(StrEnum):
    def __str__(self):
        return self.value

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)
