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
