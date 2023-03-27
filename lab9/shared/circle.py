from .point import Point
from .segment import Segment


class Circle:
    center: Point
    radius: float

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def isPassThrough(self, line: Segment) -> bool:
        a, c = line.start.toTuple()
        b, d = line.toVector().toTuple()
        r = self.radius
        x0 = self.center.x
        y0 = self.center.y
        # pure math(magic)
        det = 4*(a*b+c*d-b*x0-d*y0)**2 - 4*(b**2+d**2) * \
            (a**2+c**2-r**2-2*a*x0+x0**2-2*c*y0+y0**2)
        return det >= 0
