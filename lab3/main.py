import math
import time
from shared.point import Point
from shared.segment import Segment
from shared.polygon import Polygon
from shared.convex_polygon import ConvexPolygon
import shared.random as rand_utils
from shared.colors import COLORS
import pygame
from shared.drawers import drawPoint, drawPolygon


if __name__ == "__main__":
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 3")

    convexPolygonPoints = [
        Point(600, 453, "q0"),
        Point(414, 497, "q1"),
        Point(196, 446, "q2"),
        Point(62, 285, "q3"),
        Point(180, 84, "q4"),
        Point(600, 48, "q5"),
        Point(620, 360, "q6"),
    ]

    convexPolygon = ConvexPolygon(convexPolygonPoints)

    simplePolygonPoints = [
        Point(469, 359),
        Point(381, 300),
        Point(300, 293),
        Point(217, 280),
        Point(214, 215),
        Point(288, 240),
        Point(445, 207),
    ]

    simplePolygon = Polygon(simplePolygonPoints)

    POINT_COUNT = 100
    points = rand_utils.generateRandomPoints(POINT_COUNT, 0, 800, 0, 600)

    CORRECT_POINTS = [point for point in points if convexPolygon.contains(
        point) and not simplePolygon.contains(point)]
    print("Points in area: ", len(CORRECT_POINTS))
    velocities = [rand_utils.generateRandomVelocity() for _ in CORRECT_POINTS]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(COLORS["WHITE"])

        for point in CORRECT_POINTS:
            pygame.draw.circle(screen, COLORS["GREEN"], point.toList(), 4)
        n = len(convexPolygonPoints)

        for i, point in enumerate(convexPolygonPoints):
            pygame.draw.line(
                screen, COLORS["BLUE"], point.toList(), convexPolygonPoints[(i + 1) % n].toList())
            pygame.draw.circle(screen, COLORS["BLUE"], point.toList(), 4)

        for i, point in enumerate(simplePolygonPoints):
            pygame.draw.line(
                screen, COLORS["RED"], point.toList(), simplePolygonPoints[(i + 1) % len(simplePolygonPoints)].toList())
            pygame.draw.circle(screen, COLORS["RED"], point.toList(), 4)

        pygame.display.update()

        for point, velocity in zip(CORRECT_POINTS, velocities):
            if (velocity.x == 0 and velocity.y == 0):
                continue
            if simplePolygon.contains(point):
                velocity.clear()
                continue
            # TODO: Bug - some points can get out from Polygon

            predictedPoint = point + velocity

            if not convexPolygon.contains(predictedPoint):
                for i in range(n):
                    segment = Segment(
                        convexPolygonPoints[i], convexPolygonPoints[(i + 1) % n])

                    if segment.determinePosition(predictedPoint) > 0:
                        velocity.reflect(segment)
                        break

            point.add(velocity)
