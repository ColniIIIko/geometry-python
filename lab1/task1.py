import numpy as np
import pygame
from shared.point import Point
from shared.vector import Vector
from shared.colors import COLORS

# Task 2
# Conditions
p0 = Point(200, 200, "p0")
p1 = Point(200, 400, "p1")
p2 = Point(400, 300, "p2")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 1 - Task 2")


def drawPoint(surface: pygame.Surface, point: Point, color: tuple):
    pygame.draw.circle(surface, color, (point.x, point.y), 5)
    renderText(surface, point.caption, Vector(point.x, point.y), color)


def drawLine(surface: pygame.Surface, point1: Point, point2: Point, color: tuple):
    pygame.draw.line(surface, color, (point1.x, point1.y),
                     (point2.x, point2.y), 1)


def determinePosition(point0: Point, pointA: Point, pointB: Point):
    ABVector = pointB - pointA
    A0Vector = point0 - pointA
    det = np.linalg.det([A0Vector.toList(), ABVector.toList()])
    return det


def mapDetToPosition(det: float):
    if (det == 0):
        return "На прямой"
    elif (det < 0):
        return "Правее"
    return "Левее"


def renderText(surface: pygame.Surface, text: str, position: Vector, color: tuple):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(text, True, color)
    surface.blit(text, position.toList())


if __name__ == "__main__":

    print("Расположение p0 относительно прямой p1p2: " +
          mapDetToPosition(determinePosition(p0, p1, p2)))

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

        
