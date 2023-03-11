import math
from shared.point import Point
from shared.vector import Vector
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
import shared.random as rand_utils
import pygame
from shared.drawers import drawPoint, drawLine


def drawLines(points: list[Point]):
    for i in range(len(points)):
        drawLine(screen, points[i], points[(i+1) %
                 len(points)], COLORS["BLACK"])


def drawPoints(points: list[Point]):
    for point in points:
        drawPoint(screen, point, COLORS["BLACK"])


def getVisiblePoints(point: Point, convexHull: list[Point]):
    visible: list[int] = []
    for i in range(len(convexHull)):
        if Segment(convexHull[i], convexHull[(i + 1) % len(convexHull)]).determinePosition(point) < 0:
            visible.append(i)
            visible.append((i + 1) % len(convexHull))
    return visible


def constructHull(point: Point, convexHull: list[Point]):
    visiblePoints = getVisiblePoints(point, convexHull)
    convexHullCopy = [point for point in convexHull]
    if len(visiblePoints) == 0:
        return convexHull

    mainPoints = set()
    for index in visiblePoints:
        setSize = len(mainPoints)
        mainPoints.add(index)
        if len(mainPoints) == setSize:
            mainPoints.remove(index)

    leftPoint = mainPoints.pop()
    rightPoint = mainPoints.pop()
    if Segment(convexHull[leftPoint], convexHull[rightPoint]).determinePosition(point) < 0:
        leftPoint, rightPoint = rightPoint, leftPoint

    for i in set(visiblePoints):
        if i != leftPoint and i != rightPoint:
            convexHullCopy.remove(convexHull[i])
    convexHullCopy.insert(rightPoint + 1, point)
    return convexHullCopy


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 7")
    screen.fill(COLORS["WHITE"])

    FPS = 2
    points: list[Point] = []
    convexHull: list[Point] = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(COLORS["WHITE"])
        drawLines(convexHull)
        drawPoints(points)
        pygame.display.update()

        generatedPoint = rand_utils.generateRandomPoint(50, 750, 50, 750)
        points.append(generatedPoint)
        if len(convexHull) < 3:
            convexHull.append(generatedPoint)

            if len(convexHull) == 2:
                if convexHull[0] == convexHull[1]:
                    convexHull.pop()

            if len(convexHull) == 3:
                if convexHull[0] == convexHull[1] or convexHull[1] == convexHull[2]:
                    convexHull.pop()

                if Segment(convexHull[0], convexHull[1]).determinePosition(convexHull[2]) < 0:
                    convexHull[2], convexHull[1] = convexHull[1], convexHull[2]
                elif Segment(convexHull[0], convexHull[1]).determinePosition(convexHull[2]) == 0:
                    points.pop()
                    convexHull.pop()
        else:
            convexHull = constructHull(generatedPoint, convexHull)

        clock.tick(FPS)
