import numpy as np
import pygame
from shared.point import Point
from shared.colors import COLORS
from shared.drawers import drawPoint, drawLine
# Task 2
# Conditions
p0 = Point(200, 200, "p0")
p1 = Point(200, 400, "p1")
p2 = Point(400, 300, "p2")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 1 - Task 2")


def determinePosition(point0: Point, pointA: Point, pointB: Point) -> float:
    """
    Determines the position of point0 relative to the line AB.
    """
    ABVector = pointB - pointA
    A0Vector = point0 - pointA
    # Pygame отражает ось y, поэтому меняем знак.
    det = -1 * np.linalg.det([ABVector.toList(), A0Vector.toList()])
    return det


def mapDetToPosition(det: float) -> str:
    if (det == 0):
        return "На прямой"
    elif (det < 0):
        return "Правее"
    return "Левее"


if __name__ == "__main__":
    det = determinePosition(p0, p1, p2)
    print("Положение p0 относительно прямой p1p2: " +
          mapDetToPosition(det))

    screen.fill(COLORS["WHITE"])

    drawPoint(screen, p0, COLORS["BLACK"])
    drawPoint(screen, p1, COLORS["BLACK"])
    drawPoint(screen, p2, COLORS["BLACK"])

    drawLine(screen, p1, p2, COLORS["BLACK"])

    pygame.display.flip()
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
