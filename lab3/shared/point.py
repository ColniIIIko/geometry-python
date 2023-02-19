from .vector import Vector


class Point(Vector):
    def __init__(self, x, y, caption: str = ""):
        super().__init__(x, y)
        self.caption = caption

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
