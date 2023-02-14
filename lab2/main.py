# Task
# Определить, лежит ли точка внутри многоугольника, заданного координатами своих вершин.
# Входные данные: координаты точки и координаты вершин многоугольника.

import numpy as np
from shared.point import Point
from shared.segment import Segment
import pygame
from shared.drawers import drawPoint, drawPolygon
from shared.colors import COLORS


def isPointInPolygon(point: Point, polygon: list[Point]) -> bool:
    # Бесконечно удаленная точка
    INFINITE_POINT = Point(1000000000, point.y)
    # Проверяем, что бы точка не лежала на одной из сторон многоугольника
    for i in range(len(polygon)):
        pointA = polygon[i]
        pointB = polygon[(i + 1) % len(polygon)]

        if Segment(pointA, pointB).determinePosition(point) == 0:
            return False

    # Проверяем, что бы точка лежала внутри многоугольника
    # Для этого строим отрезок от точки до бесконечности и считаем количество пересечений с отрезками многоугольника
    # Если количество пересечений нечетное, то точка лежит внутри многоугольника
    count = 0
    for i in range(len(polygon)):
        segmentAB = Segment(polygon[i], polygon[(i + 1) % len(polygon)])
        segmentCD = Segment(point, INFINITE_POINT)
        if Segment.isIntersects(segmentAB, segmentCD):
            count += 1

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
