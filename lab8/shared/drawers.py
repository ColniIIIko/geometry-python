import pygame
from .point import Point
from .vector import Vector


def drawPoint(surface: pygame.Surface, point: Point, color: tuple):
    pygame.draw.circle(surface, color, (point.x, point.y), 5)
    text = ""
    try:
        text = point.caption
    except:
        pass
    renderText(surface, text, Vector(point.x, point.y), color)


def drawLine(surface: pygame.Surface, point1: Point, point2: Point, color: tuple, width=1):
    pygame.draw.line(surface, color, (point1.x, point1.y),
                     (point2.x, point2.y), width)


def renderText(surface: pygame.Surface, text: str, position: Vector, color: tuple):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(text, True, color)
    surface.blit(text, position.toList())


def drawPolygon(surface: pygame.Surface, points: list[Point], color: tuple, textColor=(0, 0, 0)):
    # for i in range(len(points)):
    #     drawPoint(surface, points[i], textColor)
    coordsList = [point.toTuple() for point in points]
    pygame.draw.polygon(surface, color, coordsList)
