import math
from shared.point import Point
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
import shared.random as rand_utils
import pygame
from shared.drawers import drawPoint, drawLine, drawPolygon
import numpy as np
from shared.dimensions import getDimensions, isLieInRectangle

POINT_RADIUS = 5
MAX_POINT_CHECK = 7


def dimensionalTest(point: Point, polygon: list[Point]) -> bool:
    """
    Проверяет, может ли точка находиться в многоугольнике (Габаритный тест)
    """
    xMin, xMax, yMin, yMax = getDimensions(polygon)
    return isLieInRectangle(point, xMin, xMax, yMin, yMax)


def drawPoints(points: list[Point]):
    for point in points:
        drawPoint(screen, point, COLORS["BLACK"], POINT_RADIUS)


def findClosestPoints(points: list[Point]) -> tuple[Point, Point]:
    X = [point for point in points]
    X.sort(key=lambda point: point.x)
    Y = [point for point in points]
    Y.sort(key=lambda point: point.y)
    return findRecursive(X, Y)


def tupleToDistance(tup: tuple[Point, Point]):
    point1, point2 = tup
    return (point2 - point1).length()


def findDistanceFull(points: list[Point]) -> tuple[Point, Point]:
    """
    Ищет две самые близкие точки методом полного перебора. O(n^2)
    """
    minimalDistance = math.inf
    points: tuple[Point, Point]
    for point1 in points:
        for point2 in points:
            if point1 == point2:
                continue
            distance = tupleToDistance((point1, point2))
            if distance < minimalDistance:
                minimalDistance = distance
                points = (point1, point2)

    return points


def findRecursive(X: list[Point], Y: list[Point]) -> tuple[Point, Point]:
    """
    Рекурсивная часть алгоритма нахождения двух ближайших точек.
    1. Для 3 и менее точек осуществляется полный перебор
    2. Иначе производится рекурсивное деление множества
    """
    if len(X) <= 3:
        return findDistanceFull(X)

    separator = len(X) // 2
    xLeft = X[0:separator]
    xRight = X[separator:]
    yLeft: list[Point] = []
    yRight: list[Point] = []
    for point in Y:
        if point.x < X[separator].x:
            yLeft.append(point)
        elif point.x > X[separator].x:
            yRight.append(point)
        else:
            if point in xLeft:
                yLeft.append(point)
            else:
                yRight.append(point)
    leftPoints = findRecursive(xLeft, yLeft)
    rightPoints = findRecursive(xRight, yRight)
    delta = min(leftPoints, rightPoints, key=tupleToDistance)
    deltaDistance = tupleToDistance(delta)
    yDelta: list[Point] = []
    for point in Y:
        if abs(point.x - X[separator].x) < deltaDistance:
            yDelta.append(point)

    for point in yDelta:
        count = 0
        for extraPoint in yDelta:
            if count == 7:
                break
            if point == extraPoint:
                continue

            distance = (extraPoint - point).length()
            if distance < deltaDistance:
                delta = (point, extraPoint)
            count += 1
    return delta


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 9")
    rectangle = [
        Point(50, 100, "A"),
        Point(750, 100, "B"),
        Point(750, 600, "C"),
        Point(50, 600, "D")
    ]
    FPS = 60
    xMin, xMax, yMin, yMax = getDimensions(rectangle)
    points: list[Point] = rand_utils.generateRandomPoints(
        24, xMin, xMax, yMin, yMax)
    velocities = [rand_utils.generateRandomVelocity() for _ in points]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        point1, point2 = findClosestPoints(points)
        screen.fill(COLORS["WHITE"])
        drawPoints(points)
        drawLine(screen, point1, point2, COLORS["RED"])
        drawPolygon(screen, rectangle, COLORS["BLACK"])
        pygame.display.update()

        for point, velocity in zip(points, velocities):
            predicted = point + velocity
            for i in range(len(rectangle)):
                edge = Segment(
                    rectangle[i], rectangle[(i + 1) % len(rectangle)])
                if edge.determinePosition(predicted) > 0:
                    velocity.reflect(edge)
                    break
            if (point == point1 or point == point2) and (point2 - point1).length() <= 2 * POINT_RADIUS:
                velocity.inverse()

            point.add(velocity)

        clock.tick(FPS)
