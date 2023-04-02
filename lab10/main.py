from shared.point import Point
from shared.segment import Segment
from shared.colors import COLORS
from shared.drawers import drawPoint
from shared.triangle import Triangle
import shared.random as rand_utils
import pygame
from shared.drawers import drawPoint, drawLine, drawPolygon
from shared.vector import Vector


def draw_triangle(screen: pygame.Surface, triangle: Triangle):
    for line in triangle.to_lines():
        drawLine(screen, line.start, line.end, COLORS["BLACK"])


def find_nearest_point(points: list[Point], point1: Point, point2: Point):
    max_angle = -9999
    max_pos = -1
    for i, item in enumerate(points):
        fst_vector = Vector(item.x - point1.x, item.y - point1.y)
        snd_vector = Vector(item.x - point2.x, item.y - point2.y)
        if not ((item.x == point1.x and item.y == point1.y) or (item.x == point2.x and item.y == point2.y)):
            angle = Vector.computeAngle(fst_vector, snd_vector)
            if angle > max_angle:
                max_angle = angle
                max_pos = i
    return max_pos


# первый шаг триангуляции
def start_triangulation(param_points: list[Point]):
    # находим ближайшую точку к самым нижним
    max_pos = find_nearest_point(
        param_points, param_points[0], param_points[1])
    print("Min: ", param_points[0], param_points[1])
    print("Nearest", param_points[max_pos])
    current_triangulation = []
    if Segment(param_points[0], param_points[1]).determinePosition(param_points[max_pos]) > 0:
        current_triangulation += triangulation(
            param_points, param_points[1], param_points[max_pos], current_triangulation)
        current_triangulation += triangulation(
            param_points, param_points[max_pos], param_points[0], current_triangulation)
    else:
        current_triangulation += triangulation(
            param_points, param_points[0], param_points[max_pos], current_triangulation)
        current_triangulation += triangulation(
            param_points, param_points[max_pos], param_points[1], current_triangulation)
    return [Triangle(points[p1], points[p2], points[p3])
            for p1, p2, p3 in current_triangulation]


def triangle_exist(candidate: list[int], tri: list[list[int]]):
    for item in tri:
        if item[0] == candidate[0] and item[1] == candidate[1] and item[2] == candidate[2]:
            return True
    return False


def triangulation(points: list[Point], point1: Point, point2: Point, tri: list[list[int]]):
    higher: list[Point] = [item for item in points if Segment(
        point1, point2).determinePosition(item) < 0]
    if len(higher):  # если нашлись точки, то продолжаем рекурсию
        point = find_nearest_point(
            higher, point1, point2)  # ищем ближайшую точку
        triangle = [point1.pos, point2.pos, higher[point].pos]
        triangle.sort()
        # если такого треугольника нет, то продолжаем
        if not triangle_exist(triangle, tri):
            tri.append(triangle)  # добавляем в массив треугольников

            return [triangle] + triangulation(points, point1, higher[point], tri) + triangulation(points, higher[point], point2, tri)
        return [triangle]

    return []


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lab 9")
    points: list[Point] = rand_utils.generateRandomPoints(
        8, 100, 700, 100, 700)
    points.sort(key=lambda point: point.y)
    for i, point in enumerate(points):
        point.pos = i
    screen.fill(COLORS["WHITE"])
    triangles = start_triangulation(points)
    for point in points:
        drawPoint(screen, point, COLORS["BLACK"])
    for triangle in triangles:
        draw_triangle(screen, triangle)
    print(points)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
