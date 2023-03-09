from shared.point import Point
from shared.vector import Vector
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
import shared.random as rand_utils
import pygame
import numpy as np
from shared.drawers import drawPoint, drawLine


def findMinimalYPoint(points: list[Point]) -> Point:
    foundedPoint = points[0]
    for point in points:
        if point.y < foundedPoint.y:
            foundedPoint = point
        elif point.y == foundedPoint.y and point.x < foundedPoint.x:
            foundedPoint = point
    return foundedPoint


def findMaximumYPoint(points: list[Point]) -> Point:
    foundedPoint = points[0]
    for point in points:
        if point.y > foundedPoint.y:
            foundedPoint = point
        elif point.y == foundedPoint.y and point.x < foundedPoint.x:
            foundedPoint = point
    return foundedPoint


def findMaximumXPoint(points: list[Point]) -> Point:
    foundedPoint = points[0]
    for point in points:
        if point.x > foundedPoint.x:
            foundedPoint = point
        elif point.x == foundedPoint.x and point.y < foundedPoint.y:
            foundedPoint = point
    return foundedPoint


def findMinimalXPoint(points: list[Point]) -> Point:
    foundedPoint = points[0]
    for point in points:
        if point.x < foundedPoint.x:
            foundedPoint = point
        elif point.x == foundedPoint.x and point.y > foundedPoint.y:
            foundedPoint = point
    return foundedPoint


def determineCos(startPoint: Point, endPoint: Point, direction=1) -> float:
    line = endPoint - startPoint
    xAxis = Vector(direction, 0)
    cos = Vector.scalarProduct(line, xAxis) / line.length()
    return cos


def getTriangleSquare(point1: Point, point2: Point, point3: Point) -> float:
    vector1 = point1 - point3
    vector2 = point2 - point3
    return np.abs(np.linalg.det([vector1.toList(), vector2.toList()])) / 2


def findMinHigherAngleToPoint(startPoint: Point, points: list[Point], direction=1):
    pointsCopy: list[Point] = [
        point for point in points if point != startPoint]

    minAnglePoint = startPoint
    i = 0
    while minAnglePoint.y * direction <= startPoint.y * direction and i < len(pointsCopy):
        minAnglePoint = pointsCopy[i]
        i += 1

    for point in pointsCopy:
        if determineCos(startPoint, point, direction * -1) > determineCos(startPoint, minAnglePoint, direction * -1) and direction * point.y >= direction * startPoint.y:
            minAnglePoint = point

    return minAnglePoint


def findConvexHull(points: list[Point]):
    startPoint = findMinimalYPoint(points)
    convexHull = [startPoint]
    activePoint = findMinHigherAngleToPoint(startPoint, points)
    convexHull.append(activePoint)

    direction = 1
    maxYPont = findMaximumYPoint(points)
    while activePoint != startPoint:
        if direction != -1 and activePoint == maxYPont:
            direction = -1
        activePoint = findMinHigherAngleToPoint(activePoint, points, direction)
        convexHull.append(activePoint)

    return convexHull


def getPointListDiameter(points: list[Point]):
    convexHull = findConvexHull(points)
    points
    diameter = 0
    i = 1
    while (getTriangleSquare(convexHull[-1], convexHull[0], convexHull[i]) < getTriangleSquare(convexHull[-1], convexHull[0], convexHull[i+1])):
        i += 1
    start = i
    isLapped = False
    j = 0
    while j <= len(convexHull):
        while (getTriangleSquare(convexHull[j % len(convexHull)], convexHull[(j+1) % len(convexHull)], convexHull[i]) < getTriangleSquare(convexHull[j % len(convexHull)], convexHull[(j+1) % len(convexHull)], convexHull[(i+1) % len(convexHull)])):
            i += 1
        end = i
        for k in range(start, end + 1):
            currentDiameter = (
                convexHull[j % len(convexHull)] - convexHull[k]).length()
            if diameter < currentDiameter:
                diameter = currentDiameter
                points = (convexHull[j % len(convexHull)], convexHull[k])
        start = end
        j += 1

    return points


def drawLines(points: list[Point]):
    for i in range(len(points) - 1):
        drawLine(screen, points[i], points[i+1], COLORS["BLACK"])


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 4")
    screen.fill(COLORS["WHITE"])

    POINT_COUNT = 100
    FPS = 24
    DIAMETER = 400

    points = rand_utils.generateRandomPoints(
        POINT_COUNT, 400 - DIAMETER / 2, 400 + DIAMETER / 2, 400 - DIAMETER / 2, 400 + DIAMETER / 2)
    velocities = [rand_utils.generateRandomVelocity() for _ in points]
    isFinished = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if isFinished:
            continue

        for point in points:
            drawPoint(screen, point, COLORS["BLACK"])

        pygame.display.update()

        screen.fill(COLORS["WHITE"])

        convexHull = findConvexHull(points)
        # print(convexHull)
        drawLines(convexHull)

        point1, point2 = getPointListDiameter(points)
        diameter = Vector(point2.x - point1.x, point2.y - point1.y).length()
        # print(point1.caption, point2.caption)
        # print(diameter)
        drawLine(screen, point1, point2, COLORS["RED"])
        for point, velocity in zip(points, velocities):
            if diameter > DIAMETER:
                if point == point1 or point == point2:
                    velocity.inverse()

            point.add(velocity)

        clock.tick(FPS)
