#KD-tree：
from typing import List
from collections import namedtuple
import time

class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):
    def __repr__(self):
        return f'{tuple(self)!r}'

class KDTree:
    def __init__(self):
        self._root = None
        self._n = 0

# insert()
    def insert(self, p: List[Point]):
        def rec_ins(lst: List[Point], depth: int):
            if not lst:
                return None
            axis = depth % 2
            mid = len(lst) // 2
            if axis == 0:
                lst.sort(key=lambda pt: pt.x)
            else:
                lst.sort(key=lambda pt: pt.y)
            left_lst = lst[:mid]
            right_lst = lst[mid + 1:]
            return Node(lst[mid], rec_ins(left_lst, depth + 1), rec_ins(right_lst, depth + 1))
        self._root = rec_ins(p, self._n)

 #range()
    def range(self, rectangle: Rectangle) -> List[Point]:
        result = []
        def rec_ran(rec: Rectangle, node: Node, depth: int):
            if not node:
                return None
            axis = depth % 2
            if axis == 0:
                if node.location.x < rec.lower.x:
                    rec_ran(rec, node.right, depth + 1)
                elif node.location.x > rec.upper.x:
                    rec_ran(rec, node.left, depth + 1)
                else:
                    rec_ran(rec, node.right, depth + 1)
                    rec_ran(rec, node.left, depth + 1)
                    if rec.is_contains(node.location):
                        result.append(node.location)

            else:
                if node.location.y < rec.lower.y:
                    rec_ran(rec, node.right, depth + 1)
                elif node.location.y > rec.upper.y:
                    rec_ran(rec, node.left, depth + 1)
                else:
                    rec_ran(rec, node.right, depth + 1)
                    rec_ran(rec, node.left, depth + 1)
                    if rec.is_contains(node.location):
                        result.append(node.location)

        rec_ran(rectangle, self._root, self._n)
        return result
 # K nearest neighbor query:
    def knn(self, target_pt: Point):
        path = []
        n_node = None
        dis = 0
        def distance(point: Point):
            return ((point.x - target_pt.x) ** 2 + (point.y - target_pt.y) ** 2) ** (0.5)

        def nearest_leaf(node: Node, depth: int):
            if node is None:
                return None
            path.append(node)
            if node.left is None and node.right is None:
                return None
            axis = depth % 2
            if axis == 0:
                if node.location.x <= target_pt.x:
                    nearest_leaf(node.right, depth + 1)
                else:
                    nearest_leaf(node.left, depth + 1)
            else:
                if node.location.y <= target_pt.y:
                    nearest_leaf(node.right, depth + 1)
                else:
                    nearest_leaf(node.left, depth + 1)

        nearest_leaf(self._root, 0)
        n_node = path.pop()
        dis = distance(n_node.location)


# proformance test
def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


def knn_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.knn(Point(0, 0))
    result = sorted([Point(2, 3)])
    print(result)


if __name__ == '__main__':
    range_test()
    performance_test()
    knn_test()