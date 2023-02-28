import math
import time
from shared.vector import Vector
from shared.point import Point
from shared.segment import Segment
from shared.polygon import Polygon
from shared.convex_polygon import ConvexPolygon
import shared.random as rand_utils
from shared.colors import COLORS
import pygame
from shared.drawers import drawPoint, drawPolygon, drawLine
from shared.stack import PointStack


def findMinimalYPoint(points: list[Point]) -> Point:
    foundedPoint = points[0]
    for point in points:
        if point.y < foundedPoint.y:
            foundedPoint = point
        elif point.y == foundedPoint.y and point.x < foundedPoint.x:
            foundedPoint = point
    return foundedPoint


def determineCos(startPoint: Point, endPoint: Point) -> float:
    line = endPoint - startPoint
    xAxis = Vector(1, 0)
    cos = - Vector.scalarProduct(line, xAxis) / line.length()
    return cos


def sortByAngle(points: list[Point], startPoint: Point):
    angleList = [determineCos(startPoint, point) for point in points]
    pointsCopy = [point for point in points if point != startPoint]
    pointsCopy.sort(key=lambda point: determineCos(
        startPoint, point), reverse=True)
    return pointsCopy


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 4")

    POINT_COUNT = 32
    PADDING = 50

    points = rand_utils.generateRandomPoints(
        POINT_COUNT, PADDING, 800 - PADDING, PADDING, 800 - PADDING)

    def drawPoints():
        for point in points:
            drawPoint(screen, point, COLORS["BLACK"])
    startPoint = findMinimalYPoint(points)
    SORTED_POINTS = sortByAngle(points, startPoint)
    ch = PointStack()
    ch.put(startPoint)
    ch.put(SORTED_POINTS[0])
    isCompleted = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if isCompleted:
            continue
        screen.fill(COLORS["WHITE"])
        drawPoints()
        n = len(SORTED_POINTS)
        for i in range(1, len(SORTED_POINTS)):
            for j in range(0, len(ch.items) - 1):
                drawLine(screen, ch.items[j], ch.items[j+1], COLORS["BLACK"])

            pygame.display.update()
            clock.tick(2)
            while Segment(ch.items[-2], ch.items[-1]).determinePosition(SORTED_POINTS[i]) < 0:
                extracted = ch.get()
                screen.fill(COLORS["WHITE"])
                drawPoints()
                for j in range(0, len(ch.items) - 1):
                    drawLine(screen, ch.items[j],
                             ch.items[j+1], COLORS["BLACK"])
                    pygame.display.update()

                clock.tick(2)

            ch.put(SORTED_POINTS[i])
            clock.tick(2)

        screen.fill(COLORS["WHITE"])
        isCompleted = True
        drawPoints()
        for i in range(len(ch.items)):
            drawLine(screen, ch.items[i], ch.items[(i + 1) %
                     len(ch.items)], COLORS["BLACK"])
        pygame.display.update()
