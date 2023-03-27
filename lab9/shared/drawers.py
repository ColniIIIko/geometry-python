import pygame
from .point import Point
from .vector import Vector
from .circle import Circle


def drawPoint(surface: pygame.Surface, point: Point, color: tuple, radius=5):
    pygame.draw.circle(surface, color, (point.x, point.y), radius)
    text = ""
    try:
        text = point.caption
    except:
        pass
    renderText(surface, text, Vector(point.x, point.y), color)


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


def drawCircles(surface: pygame.Surface, circles: list[Circle], color: tuple):
    for circle in circles:
        drawPoint(surface, circle.center, color)
        pygame.draw.circle(
            surface, color, circle.center.toList(), circle.radius, width=1)
