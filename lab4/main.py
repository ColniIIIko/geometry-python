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
    # TODO: Improvements of Algorithm - may not sort
    pointsCopy = [point for point in points if point != startPoint]
    pointsCopy.sort(key=lambda point: (
        point - startPoint).length(), reverse=True)
    pointsCopy.sort(key=lambda point: determineCos(
        startPoint, point), reverse=True)
    for point in pointsCopy:
        for lPoint in [aPoint for aPoint in pointsCopy if determineCos(
                startPoint, point) == determineCos(
                startPoint, aPoint)]:
            if (lPoint != point):
                pointsCopy.remove(lPoint)

    pointsCopy.append(startPoint)
    return pointsCopy


if __name__ == "__main__":
    WINDOWS_WIDTH = 800
    WINDOWS_HEIGHT = 800
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
    pygame.display.set_caption("Lab 4")
    screen.fill(COLORS["WHITE"])

    POINT_COUNT = 16
    PADDING = 50
    FPS = 3

    points = rand_utils.generateRandomPoints(
        POINT_COUNT, PADDING, WINDOWS_WIDTH - PADDING, PADDING, WINDOWS_HEIGHT - PADDING)

    def drawPoints(color=COLORS["BLACK"]):
        for point in points:
            drawPoint(screen, point, color)

    def drawLines(points: list[Point], color=COLORS["BLACK"]):
        for i in range(len(points) - 1):
            drawLine(screen, points[i], points[i+1], color)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            candidate = SORTED_POINTS[i]
            if Segment(convexHull[j - 1], convexHull[j]).determinePosition(candidate) > 0:
                convexHull.append(candidate)
                drawLine(screen, convexHull[j],
                         candidate, COLORS["BLACK"])
                clock.tick(FPS)
                j += 1
                pygame.display.update()
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
        print("Convex hull (point names only): ")
        print(", ".join([point.caption for point in convexHull]))
        for point in convexHull:
            drawPoint(screen, point, COLORS["RED"])
        pygame.display.update()

        isCompleted = True
