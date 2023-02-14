from .point import Point


class Polygon:
    points: list[Point]

    def __init__(self, points: list[Point]):
        self.points = points

    def __str__(self):
        return f"Polygon({self.points})"
