from .polygon import Polygon
from .point import Point
from .segment import Segment


class ConvexPolygon(Polygon):
    def contains(self, point: Point):
        """
        Бинарный тест принадлежности точки (для выпуклого многоугольника)
        """
        n = len(self.points)
        if -1 * Segment(self.points[0], self.points[1]).determinePosition(point) < 0 or -1 * Segment(self.points[0], self.points[n-1]).determinePosition(point) > 0:
            return False

        # TODO: Проверить, есть ли необходимость начинать индексировать с 0
        start, end = 1, n - 1
        while end - start > 1:
            center = (start + end) // 2
            if -1 * Segment(self.points[0], self.points[center]).determinePosition(point) < 0:
                end = center
            else:
                start = center
        edge = Segment(self.points[start], self.points[end])
        # Лежат ли точки p1 и point по одну сторону от полученной стороны
        return edge.determinePosition(self.points[0]) * edge.determinePosition(point) > 0
    pass

    def containsConvexPolygon(self, polygon: Polygon):
        counter = 0
        for point in polygon.points:
            if self.contains(point):
                counter += 1
        return counter == len(polygon.points)
