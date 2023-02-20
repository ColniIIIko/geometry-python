import math
from shared.vector import Vector
from shared.point import Point
from shared.segment import Segment
from shared.dimensions import dimensionalTest
from shared.polygon import Polygon
from shared.convex_polygon import ConvexPolygon
import shared.random as rand_utils
from shared.colors import COLORS
import pygame
from shared.drawers import drawPoint, drawPolygon, drawLine


def isPointInsidePolygonOctan(point: Point, polygon: list[Point]):
    octanSum = 0
    for i in range(len(polygon)):
        deltaI = (polygon[i] - point).toOctan()
        deltaIPlus = (polygon[(i+1) % len(polygon)] - point).toOctan()
        delta = deltaIPlus - deltaI
        if delta > 4:
            delta = delta - 8
        elif delta < -4:
            delta = delta + 8
        elif abs(delta) == 4:
            det = -1 * Segment(point, polygon[i]).determinePosition(
                polygon[(i+1) % len(polygon)])
            if det > 0:
                delta = 4
            elif det < 0:
                delta = -4
            else:
                # На стороне?
                return True

        octanSum += delta

    if abs(octanSum) == 8:
        return True
    elif abs(octanSum) == 0:
        return False
    raise Exception("Ошибка!")


def angle(p0: Point, pI: Point, pIPlus: Point):
    pureAngle = Vector.computeAngle(pI - p0, pIPlus - p0)
    if -1 * Segment(p0, pI).determinePosition(pIPlus) < 0:
        return -pureAngle
    return pureAngle


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 3")

    convexPolygonPoints = [
        Point(600, 453, "p0"),
        Point(414, 497, "p1"),
        Point(196, 446, "p2"),
        Point(62, 285, "p3"),
        Point(180, 84, "p4"),
        Point(600, 48, "p5"),
        Point(620, 360, "p6"),
    ]

    convexPolygon = ConvexPolygon(convexPolygonPoints)

    simplePolygonPoints = [
        Point(469, 359, "p1"),
        Point(381, 300, "p2"),
        Point(300, 293, "p3"),
        Point(217, 280, "p4"),
        Point(214, 215, "p5"),
        Point(288, 240, "p6"),
        Point(445, 207, "p7"),
    ]

    simplePolygon = Polygon(simplePolygonPoints)

    POINT_COUNT = 100
    points = rand_utils.generateRandomPoints(POINT_COUNT, 0, 800, 0, 600)

    CORRECT_POINTS = [point for point in points if convexPolygon.contains(
        point) and not simplePolygon.contains(point)]
    velocities = [rand_utils.generateRandomVelocity() for _ in CORRECT_POINTS]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(COLORS["WHITE"])

        for point in CORRECT_POINTS:
            drawPoint(screen, point, (0, 255, 0))

        drawPolygon(screen, convexPolygonPoints, COLORS["BLUE"])
        drawPolygon(screen, simplePolygonPoints, COLORS["RED"])
        n = len(convexPolygonPoints)

        for point, velocity in zip(CORRECT_POINTS, velocities):
            if simplePolygon.contains(point):
                velocity.clear()
            # TODO: Bug - some points can get out from Polygon

            predictedPoint = point + velocity

            if not convexPolygon.contains(predictedPoint):
                for i in range(n):
                    segment = Segment(
                        convexPolygonPoints[i], convexPolygonPoints[(i + 1) % n])

                    if segment.determinePosition(point) <= 0:
                        velocity.reflect(segment)

            point.add(velocity)

        pygame.display.update()
