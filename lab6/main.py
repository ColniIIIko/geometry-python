import math
from shared.point import Point
from shared.vector import Vector
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
import shared.random as rand_utils
import pygame
from shared.drawers import drawPoint, drawLine


def determineCos(startPoint: Point, endPoint: Point, direction=1) -> float:
    line = endPoint - startPoint
    xAxis = Vector(direction, 0)
    cos = Vector.scalarProduct(line, xAxis) / line.length()
    return cos


def getTriangleArea(point1: Point, point2: Point, point3: Point) -> float:
    vector1 = point1 - point3
    vector2 = point2 - point3
    return abs(vector1.x * vector2.y - vector1.y * vector2.x) / 2


def computePerimeter(points: list[Point]) -> float:
    perimeter = 0
    n = len(points)
    for i in range(len(points)):
        perimeter += (points[(i + 1) % n] - points[i]).length()
    return perimeter


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


def createConvexHull(points: list[Point], pLeft: Point, pRight: Point) -> list[Point]:
    if len(points) == 0:
        return [pLeft, pRight]
    maxAreaPoint = max(
        points, key=lambda point: getTriangleArea(pLeft, pRight, point))

    segment1 = Segment(pLeft, maxAreaPoint)
    segment2 = Segment(maxAreaPoint, pRight)

    s1 = [point for point in points if segment1.determinePosition(point) > 0]
    s2 = [point for point in points if segment2.determinePosition(point) > 0]

    return createConvexHull(s1, pLeft, maxAreaPoint) + [maxAreaPoint] + createConvexHull(s2, maxAreaPoint, pRight)


def findConvexHull(points: list[Point]):
    pLeft = min(points, key=lambda point: point.x)
    pRight = max(points, key=lambda point: point.x)
    pLRSegment = Segment(pLeft, pRight)
    pointsOnLeftSide = [
        point for point in points if pLRSegment.determinePosition(point) > 0]
    pointsOnRightSide = [
        point for point in points if pLRSegment.determinePosition(point) < 0]

    return createConvexHull(pointsOnLeftSide, pLeft, pRight) + createConvexHull(pointsOnRightSide, pRight, pLeft)


def drawLines(points: list[Point]):
    for i in range(len(points) - 1):
        drawLine(screen, points[i], points[i+1], COLORS["BLACK"])


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 6")
    screen.fill(COLORS["WHITE"])

    POINT_COUNT = 10
    FPS = 60
    MAXIMAL_PERIMETER = 1200

    points = rand_utils.generateRandomPoints(
        POINT_COUNT, 200, 600, 200, 600)
    velocities = [rand_utils.generateRandomVelocity() for _ in points]
    isFinished = False
    # print(convexHull)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if isFinished:
            continue

        for point in points:
            drawPoint(screen, point, COLORS["BLACK"])
        convexHull = findConvexHull(points)
        drawLines(convexHull)

        pygame.display.update()

        screen.fill(COLORS["WHITE"])

        perimeter = computePerimeter(convexHull)
        print("Perimeter: ", perimeter)
        for point, velocity in zip(points, velocities):
            if perimeter > MAXIMAL_PERIMETER and point in convexHull:
                velocity.inverse()

            point.add(velocity)

        clock.tick(FPS)
