import math
from shared.point import Point
from shared.vector import Vector
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
import shared.random as rand_utils
import pygame
from shared.drawers import drawPoint, drawLine, drawPolygon
from shared.convex_polygon import ConvexPolygon


def clipSegment(segment: Segment, polygon: ConvexPolygon):
    points = polygon.points
    n = len(points)
    minimalParameter = 0
    maximumParameter = 1
    for i in range(n):
        polygonEdge = Segment(points[i], points[(i + 1) % n])
        parameter = getSegmentIntersectionParameter(polygonEdge, segment)
        if parameter is None:
            continue
        if getPointClassification(segment, polygonEdge) == 'ПВ':
            minimalParameter = max(minimalParameter, parameter)
            pass
        else:
            maximumParameter = min(maximumParameter, parameter)
            pass
    newStart = segment.start * (1 - minimalParameter) + \
        segment.end * minimalParameter
    newEnd = segment.start * (1 - maximumParameter) + \
        segment.end * maximumParameter
    newSegment = Segment(
        newStart, newEnd
    )
    return newSegment


def getSegmentIntersectionParameter(AB: Segment, CD: Segment) -> float | None:
    """
    Ищет параметр (для CD) точки пересечения отрезков AB & CD
    """
    if not Segment.isIntersects(AB, CD):
        return None
    p1 = AB.start
    p3 = CD.start
    p4 = CD.end
    normalVector = AB.toVector().getLeftHandNormal()
    return - Vector.scalarProduct(p3 - p1, normalVector) / Vector.scalarProduct(p4 - p3, normalVector)


def getPointClassification(AB: Segment, pIpIPlus: Segment):
    directionalVector = pIpIPlus.toVector()
    normalVector = Vector(directionalVector.y, -directionalVector.x)
    product = Vector.scalarProduct(AB.toVector(), normalVector)
    if (product > 0):
        return "ПП"
    elif (product < 0):
        return "ПВ"
    return ""


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 8")
    screen.fill(COLORS["WHITE"])
    convexPolygonPoints = [
        Point(600, 453, "q0"),
        Point(414, 497, "q1"),
        Point(196, 446, "q2"),
        Point(62, 285, "q3"),
        Point(180, 84, "q4"),
        Point(600, 100, "q5"),
        Point(650, 360, "q6"),
    ]

    convexPolygon = ConvexPolygon(convexPolygonPoints)
    drawPolygon(screen, convexPolygonPoints, COLORS["BLACK"])
    clipper = Segment(Point(100, 200), Point(700, 600))
    drawLine(screen, clipper.start, clipper.end, COLORS["BLACK"])
    SEGMENT = clipSegment(clipper, convexPolygon)
    drawLine(screen, SEGMENT.start, SEGMENT.end, COLORS["RED"])
    pygame.display.update()
    FPS = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
