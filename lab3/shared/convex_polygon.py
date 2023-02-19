from .polygon import Polygon
from .point import Point
from .vector import Vector
from .segment import Segment


def angle(p0: Point, pI: Point, pIPlus: Point):
    pureAngle = Vector.computeAngle(pI - p0, pIPlus - p0)
    if -1 * Segment(p0, pI).determinePosition(pIPlus) < 0:
        return -pureAngle
    return pureAngle


class ConvexPolygon(Polygon):
    def contains(self, point: Point):
        # TODO: Must be fixed, now have IndexError
        polygon = self.points
        n = len(polygon)
        pointZ = (polygon[0] + polygon[n // 2]) / 2
        print("Point in polygon: ", pointZ)
        print("Source point: ", point)
        polygonWithAppendedPoint = [p for p in polygon]
        polygonWithAppendedPoint.append(polygonWithAppendedPoint[0])
        print(polygonWithAppendedPoint)
        start = 1
        end = n + 1
        while (end - start > 1):
            center = (start + end) // 2
            print("Center is ", center)
            if angle(polygonWithAppendedPoint[0], pointZ, point) < angle(polygonWithAppendedPoint[0], pointZ, polygonWithAppendedPoint[center]):
                end = center
            else:
                start = center

        print(start, end)
        return not Segment.isIntersects(
            Segment(polygonWithAppendedPoint[start],
                    polygonWithAppendedPoint[end]),
            Segment(point, pointZ)
        )
