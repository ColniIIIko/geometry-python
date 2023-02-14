# Task
# Определить, лежит ли точка внутри многоугольника, заданного координатами своих вершин.
# Входные данные: координаты точки и координаты вершин многоугольника.

import numpy as np
from shared.point import Point
from shared.segment import Segment
import pygame
from shared.drawers import drawPoint, drawPolygon
from shared.colors import COLORS


def testDimensional(point: Point, polygon: list[Point]) -> bool:
    xList = [point.x for point in polygon]
    xMax = np.max(xList)
    xMin = np.min(xList)

    yList = [point.y for point in polygon]
    yMax = np.max(yList)
    yMin = np.min(yList)

    if point.x < xMin or point.x > xMax or point.y < yMin or point.y > yMax:
        return True
    else:
        return False


def isPointInPolygon(point: Point, polygon: list[Point]) -> bool:

    if testDimensional(point, polygon):
        return False

    xMin = np.min([point.x for point in polygon])
    pointQ = Point(xMin - 1, point.y)

    # Проверяем, что бы точка не лежала на одной из сторон многоугольника

    for i in range(len(polygon)):
        pointA = polygon[i]
        pointB = polygon[(i + 1) % len(polygon)]

        if Segment(pointA, pointB).determinePosition(point) == 0:
            return False

    # Проверяем, что бы точка лежала внутри многоугольника
    # Для этого строим отрезок от точки до бесконечности и считаем количество пересечений с отрезками многоугольника
    # Если количество пересечений нечетное, то точка лежит внутри многоугольника
    segmentCD = Segment(point, pointQ)
    count = 0
    for i in range(len(polygon)):
        segmentAB = Segment(polygon[i], polygon[(i + 1) % len(polygon)])
        if Segment.isIntersects(segmentAB, segmentCD):
            if (not segmentCD.isPointLie(polygon[i]) and not segmentCD.isPointLie(polygon[(i + 1) % len(polygon)])):
                count += 1
            else:
                if segmentCD.isPointLie(polygon[i]):
                    j = i - 1
                    while segmentCD.isPointLie(polygon[j]):
                        j -= 1
                        if j < 0:
                            j += len(polygon)
                    k = i + 1
                    while segmentCD.isPointLie(polygon[k]):
                        k += 1
                        if k >= len(polygon):
                            k -= len(polygon)
                    pointK = polygon[k]
                    pointJ = polygon[j]
                    pointKPosition = segmentCD.determinePosition(pointK)
                    pointJPosition = segmentCD.determinePosition(pointJ)
                    if (pointKPosition*pointJPosition <= 0):
                        count += 1
                    i = k
                elif segmentCD.isPointLie(polygon[(i+1) % len(polygon)]):
                    j = i
                    while segmentCD.isPointLie(polygon[j]):
                        j -= 1
                        if j < 0:
                            j += len(polygon)
                    k = i + 2
                    while segmentCD.isPointLie(polygon[k]):
                        k += 1
                        if k >= len(polygon):
                            k -= len(polygon)
                    pointK = polygon[k]
                    pointJ = polygon[j]
                    pointKPosition = segmentCD.determinePosition(pointK)
                    pointJPosition = segmentCD.determinePosition(pointJ)
                    if (pointKPosition*pointJPosition <= 0):
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
    point = Point(460, 150, "p0")

    drawPolygon(screen, polygon, COLORS["BLACK"])
    drawPoint(screen, point, COLORS["RED"])

    if isPointInPolygon(point, polygon):
        print("Точка лежит внутри многоугольника")
    else:
        print("Точка не лежит внутри многоугольника")

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
