from .point import Point


class PointStack:
    items: list[Point] = []

    def __init__(self) -> None:
        pass

    def put(self, point: Point) -> None:
        self.items.append(point)

    def get(self) -> Point:
        return self.items.pop()
