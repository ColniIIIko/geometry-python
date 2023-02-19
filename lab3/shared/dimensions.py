from .point import Point
import numpy as np


def getDimensions(polygon: list[Point]) -> tuple[float, float, float, float]:
    xList = [point.x for point in polygon]
    xMax = np.max(xList)
    xMin = np.min(xList)

    yList = [point.y for point in polygon]
    yMax = np.max(yList)
    yMin = np.min(yList)

    return xMin, xMax, yMin, yMax


def isLieInRectangle(point: Point, xMin: float, xMax: float, yMin: float, yMax: float) -> bool:
    if point.x < xMin or point.x > xMax or point.y < yMin or point.y > yMax:
        return False
    else:
        return True


def dimensionalTest(point: Point, polygon: list[Point]) -> bool:
    xMin, xMax, yMin, yMax = getDimensions(polygon)
    return isLieInRectangle(point, xMin, xMax, yMin, yMax)
