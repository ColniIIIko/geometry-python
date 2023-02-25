from .polygon import Polygon
from .point import Point
from .vector import Vector
from .segment import Segment


def angle(p0: Point, pI: Point, pIPlus: Point):
    pureAngle = Vector.computeAngle(pI - p0, pIPlus - p0)
    if Segment(p0, pI).determinePosition(pIPlus) < 0:
        return -pureAngle
    return pureAngle


class ConvexPolygon(Polygon):
    def contains(self, point: Point):
        n = len(self.points)
        if -1 * Segment(self.points[0], self.points[1]).determinePosition(point) < 0 or -1 * Segment(self.points[0], self.points[n-1]).determinePosition(point) > 0:
            return False

        start, end = 1, n - 1
        while end - start > 1:
            center = (start + end) // 2
            if -1 * Segment(self.points[0], self.points[center]).determinePosition(point) < 0:
                end = center
            else:
                start = center

        return not Segment.isIntersects(Segment(self.points[start], self.points[end]), Segment(self.points[0], point))
    pass
