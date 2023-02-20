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
    # TODO: Must be implemented
    # def contains(self, point: Point):
    #     polygon = self.points
    #     n = len(polygon)
    #     pointZ = (polygon[n // 2] + polygon[0]) / 2

    #     polygonWithAppendedPoint = [p for p in polygon]
    #     polygonWithAppendedPoint.append(polygonWithAppendedPoint[0])
    #     point1 = polygon[0]
    #     start = 0
    #     end = n
    #     while (end - start > 1):
    #         center = int((start + end) / 2)
    #         if angle(point1, pointZ, point) < angle(point1, pointZ, polygonWithAppendedPoint[center]):
    #             end = center
    #         else:
    #             start = center
    #     print(start, end)
    #     return angle(polygonWithAppendedPoint[start], polygonWithAppendedPoint[end], point) < 0

    pass
