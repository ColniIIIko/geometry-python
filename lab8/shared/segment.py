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

    def toVector(self):
        return Vector(self.end.x - self.start.x, self.end.y - self.start.y)

    @staticmethod
    def isIntersects(segment1: Segment, segment2: Segment) -> bool:
        """
        Определяет, пересекаются ли отрезки
        """
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

    @staticmethod
    def isCollinear(segment1: Segment, segment2: Segment):
        vector1 = segment1.toVector()
        vector2 = segment2.toVector()

        if vector2.y != 0 and vector1.y != 0:
            return vector1.x / vector1.y == vector2.x / vector2.y

        return vector2.y == vector1.y

    def determinePosition(self, point: Point) -> float:
        """
        Определяет положение точки относительно текущего отрезка
        """
        ABVector = self.end - self.start
        A0Vector = point - self.start
        return A0Vector.x * ABVector.y - A0Vector.y * ABVector.x
        det = np.linalg.det([A0Vector.toList(), ABVector.toList()])
        return det

    def isPointLie(self, point: Point) -> bool:
        """
        Проверят, лежит ли точка на отрезке (включая концы)
        """
        return Vector.scalarProduct(self.start - point, self.end - point) <= 0 and self.determinePosition(point) == 0

    def isAimedAt(self, segment: Segment) -> bool:
        a = self.toVector()
        b = segment.toVector()
        det = b.x * a.y - b.y * a.x

        if Segment.isCollinear(self, segment):  # проверка на коллинеарность
            checkVector = segment.end - self.end
            checkVector2 = segment.start - self.end
            cos = Vector.scalarProduct(
                checkVector, a)
            cos2 = Vector.scalarProduct(
                checkVector2, a)
            return cos > 0 and cos2 < 0

        isInside = segment.determinePosition(self.end) <= 0
        if isInside:
            return det < 0
        else:
            return det >= 0
