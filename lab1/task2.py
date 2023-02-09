import numpy as np
import pygame
from shared.point import Point
from shared.vector import Vector
from shared.colors import COLORS
from task1 import determinePosition

# Task 2
# Conditions

p1 = Point(300, 100, "p1")
p2 = Point(400, 200, "p2")
p3 = Point(400, 50, "p3")
p4 = Point(400, 400, "p4")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 1 - Task 2")


def drawPoint(surface: pygame.Surface, point: Point, color: tuple):
    pygame.draw.circle(surface, color, (point.x, point.y), 5)
    renderText(surface, point.caption, Vector(point.x, point.y), color)


def drawLine(surface: pygame.Surface, point1: Point, point2: Point, color: tuple):
    pygame.draw.line(surface, color, (point1.x, point1.y),
                     (point2.x, point2.y), 1)


def renderText(surface: pygame.Surface, text: str, position: Vector, color: tuple):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(text, True, color)
    surface.blit(text, position.toList())


def scalarProduct(vectorA: Vector, vectorB: Vector):
    """
    Computes the scalar product of two vectors.
    """
    return np.dot(vectorA.toList(), vectorB.toList())


def isSegmentsIntersect(pointA: Point, pointB: Point, pointC: Point, pointD: Point):
    det1 = determinePosition(pointA, pointC, pointD)
    det2 = determinePosition(pointB, pointC, pointD)
    det3 = determinePosition(pointC, pointA, pointB)
    det4 = determinePosition(pointD, pointA, pointB)

    if det1 == 0 and det2 == 0 and det3 == 0 and det4 == 0:
        # Значит точки лежат на прямой
        # Проверяем, что бы отрезки накладывались друг на друга

        # Точка A лежит на отрезке CD?
        sc1 = scalarProduct(pointC - pointA, pointD - pointA)
        # Точка C лежит на отрезке AB?
        sc2 = scalarProduct(pointC - pointB, pointC - pointA)
        # Точка D лежит на отрезке AB?
        sc3 = scalarProduct(pointD - pointA, pointD - pointB)

        if sc1 < 0 or sc2 < 0 or sc3 < 0:
            return True

    elif det1 * det2 <= 0 and det3 * det4 <= 0:
        return True

    return False


if __name__ == "__main__":
    print("Пересекаются ли отрезки p1p2 p3p4?",
          "Да" if isSegmentsIntersect(p1, p2, p3, p4) else "Нет")

    screen.fill(COLORS["WHITE"])

    drawPoint(screen, p1, COLORS["BLACK"])
    drawPoint(screen, p2, COLORS["BLACK"])
    drawPoint(screen, p3, COLORS["BLACK"])
    drawPoint(screen, p4, COLORS["BLACK"])

    drawLine(screen, p1, p2, COLORS["BLACK"])
    drawLine(screen, p3, p4, COLORS["BLACK"])
    pygame.display.flip()
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
