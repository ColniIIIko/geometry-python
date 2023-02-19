import pygame
from .point import Point
from .vector import Vector


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


def drawPolygon(surface: pygame.Surface, points: list[Point], color: tuple):
    for i in range(len(points)):
        drawPoint(surface, points[i], color)
        drawLine(surface, points[i], points[(i + 1) % len(points)], color)
