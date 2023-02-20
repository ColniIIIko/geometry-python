# Task
# Определить, лежит ли точка внутри многоугольника, заданного координатами своих вершин.
# Входные данные: координаты точки и координаты вершин многоугольника.

import numpy as np
from shared.point import Point
from shared.segment import Segment
import pygame
from shared.drawers import drawPoint, drawPolygon
from shared.colors import COLORS


def getDimensions(polygon: list[Point]) -> tuple[float, float, float, float]:
    """
    Возвращает "габариты" указанного многоугольника
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
    Проверяет, лежит ли точка внутри указанного прямоугольника
    """
    if point.x < xMin or point.x > xMax or point.y < yMin or point.y > yMax:
        return False
    else:
        return True


def isPointInsidePolygon(point: Point, polygon: list[Point]) -> bool:
    """
    Проверяет принадлежность точки многоугольнику

    Алгоритмы:
    - Габаритный тест O(n)
    - Лучевой тест O(n)
    """
    xMin, xMax, yMin, yMax = getDimensions(polygon)
    if not isLieInRectangle(point, xMin, xMax, yMin, yMax):
        return False

    rayFromPoint = Segment(point, Point(xMin - 1, point.y))
    count = 0
    for i in range(len(polygon)):
        segmentAB = Segment(polygon[i], polygon[(i + 1) % len(polygon)])
        if Segment.isIntersects(segmentAB, rayFromPoint):
            if (not rayFromPoint.isPointLie(polygon[i]) and not rayFromPoint.isPointLie(polygon[(i + 1) % len(polygon)])):
                count += 1
            else:
                j = 0
                k = 0
                if rayFromPoint.isPointLie(polygon[i]):
                    j = i - 1
                    k = i + 1

                elif rayFromPoint.isPointLie(polygon[(i + 1) % len(polygon)]):
                    j = i
                    k = i + 2

                while rayFromPoint.isPointLie(polygon[j]):
                    # Ищем ближайшую из предыдущих вершин, которая не лежит на отрезке
                    j -= 1
                    if j < 0:
                        j += len(polygon)
                while rayFromPoint.isPointLie(polygon[k]):
                    # Ищем ближайшую из следующих вершин, которая не лежит на отрезке
                    k += 1
                    if k >= len(polygon):
                        k -= len(polygon)
                pointK = polygon[k]
                pointJ = polygon[j]
                pointKPosition = rayFromPoint.determinePosition(pointK)
                pointJPosition = rayFromPoint.determinePosition(pointJ)
                if (pointKPosition * pointJPosition <= 0):
                    # Если две точки лежат по разные стороны от отрезка, то учитываем пересечение
                    count += 1
                i = k

    return count % 2 == 1


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lab 2")
    screen.fill(COLORS["WHITE"])

    polygon = [
        Point(50, 50, "p1"),
        Point(100, 150, "p2"),
        Point(200, 50, "p3"),
        Point(300, 150, "p4"),
        Point(350, 50, "p5"),
        Point(400, 200, "p6"),
        Point(500, 100, "p7"),
        Point(500, 500, "p8"),
        Point(350, 150, "p9"),
        Point(250, 300, "p10"),
        Point(150, 150, "p11"),
        Point(100, 300, "p12"),
    ]
    point = Point(250, 150, "p0")

    drawPolygon(screen, polygon, COLORS["BLACK"])
    drawPoint(screen, point, COLORS["RED"])

    if isPointInsidePolygon(point, polygon):
        print("Точка лежит внутри многоугольника")
    else:
        print("Точка не лежит внутри многоугольника")

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
