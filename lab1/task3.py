from shared.polygon import Polygon
from shared.point import Point
from shared.colors import COLORS
from shared.drawers import drawPolygon
from task2 import isSegmentsIntersect
import pygame


points = [
    Point(200, 100, "p1"),
    Point(400, 150, "p2"),
    Point(200, 250, "p3"),
    Point(400, 200, "p4"),
    Point(100, 100, "p5"),
    Point(300, 50, "p6"),
]


def isComplexPolygon(polygon: Polygon) -> bool:
    """
    Проверяет, является ли многоугольник сложным
    """
    for i in range(len(polygon.points)):
        pointA = polygon.points[i % len(polygon.points)]
        pointB = polygon.points[(i + 1) % len(polygon.points)]
        for j in range(i + 2, len(polygon.points)):
            iterations += 1
            if (j + 1) % len(polygon.points) == i:
                continue
            pointC = polygon.points[j % len(polygon.points)]
            pointD = polygon.points[(j + 1) % len(polygon.points)]
            if isSegmentsIntersect(pointA, pointB, pointC, pointD):
                return True
    return False


# Task 3
if __name__ == "__main__":
    polygon = Polygon(points)
    print("Является ли многоугольник простым? ",
          "Да" if not isComplexPolygon(polygon) else "Нет")
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lab 1 - Task 3")

    screen.fill(COLORS["WHITE"])

    drawPolygon(screen, polygon.points, COLORS["BLACK"])
    pygame.display.flip()

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
