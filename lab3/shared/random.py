import math
import random
from .vector import Vector
from .constants import BASE_SPEED
from .point import Point


def generateRandomVelocity() -> Vector:
    randomAngle = random.uniform(0, 2 * math.pi)
    return Vector(BASE_SPEED * math.cos(randomAngle), BASE_SPEED * math.sin(BASE_SPEED))


def generateRandomVelocities(count: int) -> list[Vector]:
    return [
        generateRandomVelocity for _ in range(count)
    ]


def generateRandomPoints(count: int, minX: int, maxX: int, minY: int, maxY: int) -> list[Point]:
    return [
        generateRandomPoint(minX, maxX, minY, maxY, _) for _ in range(count)
    ]


def generateRandomPoint(minX: int, maxX: int, minY: int, maxY: int, index: int = None) -> Point:
    return Point(
        random.randint(minX, maxX),
        random.randint(minY, maxY),
        # "g" + str(index) if index is not None else None
    )
