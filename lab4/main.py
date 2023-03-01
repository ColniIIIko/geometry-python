from shared.vector import Vector
from shared.point import Point
from shared.segment import Segment
import shared.random as rand_utils
from shared.colors import COLORS
import pygame
from shared.drawers import drawPoint, drawLine


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
    cos = -Vector.scalarProduct(line, xAxis) / line.length()
    return cos


def sortByAngle(points: list[Point], startPoint: Point):
    pointsCopy = [point for point in points if point != startPoint]
    pointsCopy.sort(key=lambda point: determineCos(
        startPoint, point), reverse=True)
    pointsCopy.append(startPoint)
    return pointsCopy


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 4")
    screen.fill(COLORS["WHITE"])

    POINT_COUNT = 16
    PADDING = 50
    FPS = 2

    points = rand_utils.generateRandomPoints(
        POINT_COUNT, PADDING, 800 - PADDING, PADDING, 800 - PADDING)

    def drawPoints():
        for point in points:
            drawPoint(screen, point, COLORS["BLACK"])

    def drawLines(points: list[Point]):
        for i in range(len(points) - 1):
            drawLine(screen, points[i], points[i+1], COLORS["BLACK"])

    startPoint = findMinimalYPoint(points)
    SORTED_POINTS = sortByAngle(points, startPoint)
    convexHull = [startPoint, SORTED_POINTS[0]]

    drawPoints()
    drawLines(convexHull)
    isCompleted = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if isCompleted:
            continue
        i, j = 1, 1
        while i < len(SORTED_POINTS):
            candidate = SORTED_POINTS[i]
            if Segment(convexHull[j - 1], convexHull[j]).determinePosition(candidate) > 0:
                convexHull.append(candidate)
                drawLine(screen, convexHull[j],
                         candidate, COLORS["BLACK"])
                clock.tick(FPS)
                pygame.display.update()
                j += 1
            else:
                i -= 1
                j -= 1
                convexHull.pop()
                screen.fill(COLORS["WHITE"])
                drawPoints()
                drawLines(convexHull)
                clock.tick(FPS)
                pygame.display.update()
            i += 1

        pygame.display.update()
        print("Convex hull: ")
        for point in convexHull:
            print(point, end=" ")

        print()
        isCompleted = True
