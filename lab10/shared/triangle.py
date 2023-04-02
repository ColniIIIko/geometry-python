from .point import Point
from .segment import Segment

class Triangle:
    p1: Point
    p2: Point
    p3: Point
    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def to_lines(self) -> list[Segment]:
        return [Segment(self.p1, self.p2), Segment(self.p2, self.p3), Segment(self.p3, self.p1)]