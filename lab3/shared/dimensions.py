from .point import Point
import numpy as np


def getDimensions(polygon: list[Point]) -> tuple[float, float, float, float]:
    """
    Возвращает координаты в формате xMin, xMax, yMin, yMax прямоугольника, содержащего все точки
    """
    xList = [point.x for point in polygon]
    xMax = np.max(xList)
    xMin = np.min(xList)

    yList = [point.y for point in polygon]
    yMax = np.max(yList)
    yMin = np.min(yList)

    return xMin, xMax, yMin, yMax


def isLieInRectangle(point: Point, xMin: float, xMax: float, yMin: float, yMax: float) -> bool:
    """
    Проверят, лежит ли точка в прямоугольнике заданных характеристик
    """
    if point.x < xMin or point.x > xMax or point.y < yMin or point.y > yMax:
        return False
    else:
        return True


def dimensionalTest(point: Point, polygon: list[Point]) -> bool:
    """
    Проверяет, может ли точка находиться в многоугольнике (Габаритный тест)
    """
    xMin, xMax, yMin, yMax = getDimensions(polygon)
    return isLieInRectangle(point, xMin, xMax, yMin, yMax)
