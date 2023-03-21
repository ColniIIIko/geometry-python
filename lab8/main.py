from shared.point import Point
from shared.vector import Vector
from shared.segment import Segment
from shared.colors import COLORS
import pygame
from shared.drawers import drawLine, drawPolygon
from shared.convex_polygon import ConvexPolygon


def clipSegment(segment: Segment, polygon: ConvexPolygon):
    points = polygon.points
    n = len(points)
    minimalParameter = 0
    maximumParameter = 1
    isIntersect = False
    for i in range(n):
        polygonEdge = Segment(points[i], points[(i + 1) % n])
        parameter = getSegmentIntersectionParameter(polygonEdge, segment)
        if parameter is None:
            continue
        isIntersect = True
        classification = getPointClassification(segment, polygonEdge)
        if classification == 'ПВ':
            minimalParameter = max(minimalParameter, parameter)
            pass
        elif classification == 'ПП':
            maximumParameter = min(maximumParameter, parameter)
            pass

    if minimalParameter > maximumParameter:
        return None

    if not isIntersect and not polygon.contains(segment.start) and not polygon.contains(segment.end):
        return None

    newStart = segment.start * (1 - minimalParameter) + \
        segment.end * minimalParameter
    newEnd = segment.start * (1 - maximumParameter) + \
        segment.end * maximumParameter
    newSegment = Segment(
        newStart, newEnd
    )
    return newSegment


def clipPolygon(polygonP: ConvexPolygon, polygonQ: ConvexPolygon):
    points: list[Point] = []
    edgesP = polygonP.getEdges()
    edgesQ = polygonQ.getEdges()
    currentIndexP: int = 0
    currentIndexQ: int = 0
    # for indexP, edgeP in enumerate(edgesP):
    #     for indexQ, edgeQ in enumerate(edgesQ):
    #         point = getSegmentIntersectionPoint(edgeP, edgeQ)
    #         if point is not None:
    #             currentIndexP = indexP
    #             currentIndexQ = indexQ

    isOver = False
    i = 0
    while not isOver and i < 2 * (len(edgesP) + len(edgesQ)):
        currentIndexQ = currentIndexQ % len(edgesQ)
        currentIndexP = currentIndexP % len(edgesP)
        currentEdgeQ = edgesQ[currentIndexQ]
        currentEdgeP = edgesP[currentIndexP]
        if currentEdgeP.isAimedAt(currentEdgeQ):
            if currentEdgeQ.isAimedAt(currentEdgeP):
                if polygonP.contains(currentEdgeQ.end) or currentEdgeQ.determinePosition(currentEdgeP.end) >= 0:
                    currentIndexP += 1
                else:
                    currentIndexQ += 1
            else:
                if polygonQ.contains(currentEdgeP.end):  # !!!
                    points.append(currentEdgeP.end)
                currentIndexP += 1
        else:
            if currentEdgeQ.isAimedAt(currentEdgeP):
                if polygonP.contains(currentEdgeQ.end):
                    points.append(currentEdgeQ.end)
                currentIndexQ += 1
            else:
                point = getSegmentIntersectionPoint(currentEdgeP, currentEdgeQ)
                if point is not None:
                    points.append(point)
                if polygonP.contains(currentEdgeQ.end) or currentEdgeQ.determinePosition(currentEdgeP.end) >= 0:
                    currentIndexP += 1
                else:
                    currentIndexQ += 1
        i += 1
        if len(points) >= 3 and points[0] == points[-1]:
            isOver = True

    return points if len(points) != 0 else None


def getSegmentIntersectionPoint(AB: Segment, CD: Segment) -> Point | None:
    parameter = getSegmentIntersectionParameter(AB, CD)
    if parameter is None:
        return None
    vector = CD.start * (1 - parameter) + CD.end * parameter
    return Point(vector.x, vector.y)


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
    return -Vector.scalarProduct(p3 - p1, normalVector) / Vector.scalarProduct(p4 - p3, normalVector)


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
    convexPolygonPoints = [
        Point(600, 453, "q0"),
        Point(414, 497, "q1"),
        Point(196, 446, "q2"),
        Point(100, 285, "q3"),
        Point(180, 84, "q4"),
        Point(600, 100, "q5"),
        Point(650, 360, "q6"),
    ]

    convexPolygonPoints2 = [
        Point(530, 550, "p0"),
        Point(430, 380, "p1"),
        Point(410, 290, "p2"),
        Point(650, 253, "p3"),
        Point(700, 400, "p3"),
    ]

    # screen.fill(COLORS["WHITE"])

    # convexPolygon = ConvexPolygon(convexPolygonPoints)
    # convexPolygon2 = ConvexPolygon(convexPolygonPoints2)
    # clipPolygonPoints = clipPolygon(convexPolygon2, convexPolygon)
    # drawPolygon(screen, convexPolygonPoints, COLORS["YELLOW"])
    # drawPolygon(screen, convexPolygonPoints2, COLORS["BLUE"])
    # if clipPolygonPoints is not None:
    #     drawPolygon(screen, clipPolygonPoints, COLORS["GREEN"])
    # clipper = Segment(convexPolygonPoints[1], convexPolygonPoints[3])
    # drawLine(screen, clipper.start, clipper.end, COLORS["BLACK"], 3)
    # SEGMENT = clipSegment(clipper, convexPolygon2)
    # if SEGMENT is not None:
    #     drawLine(screen, SEGMENT.start, SEGMENT.end, COLORS["RED"], 3)
    # pygame.display.update()

    velocity = Vector(1.5, 1.5)
    velocity2 = Vector(-3, 0.5)
    FPS = 24
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(COLORS["WHITE"])

        convexPolygon = ConvexPolygon(convexPolygonPoints)
        convexPolygon2 = ConvexPolygon(convexPolygonPoints2)
        clipPolygonPoints = clipPolygon(convexPolygon2, convexPolygon)

        drawPolygon(screen, convexPolygonPoints, COLORS["YELLOW"])
        drawPolygon(screen, convexPolygonPoints2, COLORS["BLUE"])
        if clipPolygonPoints is not None:
            drawPolygon(screen, clipPolygonPoints, COLORS["GREEN"])

        clipper = Segment(convexPolygonPoints[1], convexPolygonPoints[3])
        drawLine(screen, clipper.start, clipper.end, COLORS["BLACK"], 3)

        SEGMENT = clipSegment(clipper, convexPolygon2)
        if SEGMENT is not None:
            drawLine(screen, SEGMENT.start, SEGMENT.end, COLORS["RED"], 3)

        pygame.display.update()
        for point in convexPolygonPoints:
            point.add(velocity)
            if point.x >= 800 or point.y >= 800 or point.x <= 0 or point.y <= 0:
                velocity.inverse()

        for point in convexPolygonPoints2:
            point.add(velocity2)
            if point.x >= 800 or point.y >= 800 or point.x <= 0 or point.y <= 0:
                velocity2.inverse()

        clock.tick(FPS)
