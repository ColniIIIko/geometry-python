from __future__ import annotations
import math
import numpy as np


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: Vector) -> None:
        self.x += other.x
        self.y += other.y

    def clear(self):
        self.x = 0
        self.y = 0

    def reflect(self, segment) -> None:
        segmentVector: Vector = segment.toVector()
        kf = 2 * Vector.scalarProduct(self,
                                      segmentVector) / Vector.scalarProduct(segmentVector, segmentVector)

        x, y = kf * segmentVector.x - self.x, kf * segmentVector.y - self.y
        self.x = x
        self.y = y

    def __add__(self, other) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, number: float) -> Vector:
        return Vector(self.x / number, self.y / number)

    def __mul__(self, number: float):
        return Vector(self.x * number, self.y * number)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def toList(self):
        return [self.x, self.y]

    def toTuple(self):
        return self.x, self.y

    def length(self):
        return math.sqrt(Vector.scalarProduct(self, self))

    @staticmethod
    def scalarProduct(vector1: Vector, vector2: Vector) -> float:
        return np.dot(vector1.toList(), vector2.toList())

    @staticmethod
    def computeAngle(vector1: Vector, vector2: Vector):
        length1 = vector1.length()
        length2 = vector2.length()
        ca = Vector.scalarProduct(vector1, vector2) / (length1 * length2)
        return math.acos(ca)

    def toOctan(self):
        x, y = self.toTuple()
        if x == 0 and y == 0:
            return 0
        if 0 <= y < x:
            return 1
        if 0 < x <= y:
            return 2
        if -y <= x <= 0:
            return 3
        if 0 < y <= -x:
            return 4
        if x < y <= 0:
            return 5
        if y <= x < 0:
            return 6
        if 0 <= x < -y:
            return 7
        if -x <= y < 0:
            return 8
        return 0
