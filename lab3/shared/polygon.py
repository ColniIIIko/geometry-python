from .point import Point
from .segment import Segment
from .dimensions import dimensionalTest


class Polygon:
    points: list[Point]

    def __init__(self, points: list[Point]):
        self.points = points

    def __str__(self):
        return f"Polygon({self.points})"

    def contains(self, point: Point):
        if not dimensionalTest(point, self.points):
            return False
        polygon = self.points
        octanSum = 0
        for i in range(len(polygon)):
            deltaI = (polygon[i] - point).toOctan()
            deltaIPlus = (polygon[(i+1) % len(polygon)] - point).toOctan()
            delta = deltaIPlus - deltaI
            if delta > 4:
                delta = delta - 8
            elif delta < -4:
                delta = delta + 8
            elif abs(delta) == 4:
                det = -1 * Segment(point, polygon[i]).determinePosition(
                    polygon[(i+1) % len(polygon)])
                if det > 0:
                    delta = 4
                elif det < 0:
                    delta = -4
                else:
                    # На стороне?
                    return True

            octanSum += delta

        if abs(octanSum) == 8:
            return True
        elif abs(octanSum) == 0:
            return False
        raise Exception("Ошибка!")
