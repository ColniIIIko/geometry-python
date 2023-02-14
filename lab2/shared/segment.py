from __future__ import annotations
from .point import Point
import numpy as np
from .vector import Vector


class Segment:
    start: Point
    end: Point

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    @staticmethod
    def isIntersects(segment1: Segment, segment2: Segment) -> bool:
        pointA = segment1.start
        pointB = segment1.end
        pointC = segment2.start
        pointD = segment2.end

        det1 = segment2.determinePosition(pointA)
        det2 = segment2.determinePosition(pointB)
        det3 = segment1.determinePosition(pointC)
        det4 = segment1.determinePosition(pointD)

        if det1 == 0 and det2 == 0 and det3 == 0 and det4 == 0:
            # Значит точки лежат на прямой
            # Проверяем, что бы отрезки накладывались друг на друга

            # Точка A лежит на отрезке CD?
            sc1 = Vector.scalarProduct(pointC - pointA, pointD - pointA)
            # Точка C лежит на отрезке AB?
            sc2 = Vector.scalarProduct(pointC - pointB, pointC - pointA)
            # Точка D лежит на отрезке AB?
            sc3 = Vector.scalarProduct(pointD - pointA, pointD - pointB)

            if sc1 < 0 or sc2 < 0 or sc3 < 0:
                return True

        elif det1 * det2 <= 0 and det3 * det4 <= 0:
            return True

        return False

    def determinePosition(self, point: Point):
        ABVector = self.end - self.start
        A0Vector = point - self.start
        det = np.linalg.det([A0Vector.toList(), ABVector.toList()])
        return det

    def isPointLie(self, point: Point) -> bool:
        return Vector.scalarProduct(self.start - point, self.end - point) <= 0 and self.determinePosition(point) == 0
