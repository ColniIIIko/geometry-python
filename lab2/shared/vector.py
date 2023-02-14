from __future__ import annotations
import numpy as np


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def toList(self):
        return [self.x, self.y]

    def toTuple(self):
        return self.x, self.y

    @staticmethod
    def scalarProduct(vector1: Vector, vector2: Vector):
        return np.dot(vector1.toList(), vector2.toList())
