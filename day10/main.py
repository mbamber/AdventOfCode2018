#! /usr/bin
# -*- coding: UTF-8 -*-

import re

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()


    grid = Grid()

    expr = 'position=<\s*(-?\d+), \s*(-?\d+)> velocity=<\s*(-?\d+), \s*(-?\d+)>'
    expr = re.compile(expr)
    for line in file_contents:
        parts = map(int, list(re.findall(expr, line)[0]))
        p = Point(parts[0], parts[1], parts[2], parts[3])
        grid.add_point(p)

    print 'Board at time {time} has dimensions {x}x{y}'.format(
        time=grid.time(),
        x=grid.dim_x(),
        y=grid.dim_y()
    )
    while not grid.all_points_touch():
        grid.step()
        print 'Board at time {time} has dimensions {x}x{y}'.format(
            time=grid.time(),
            x=grid.dim_x(),
            y=grid.dim_y()
        )

    print 'Board at time {time}:'.format(
        time=grid.time()
    )
    grid.draw()

class Grid:

    def __init__(self):
        self._points = []
        self._time = 0

    def add_point(self, point):
        self._points.append(point)

    def step(self):
        self._time += 1
        for p in self._points:
            p.step()

    def char_at(self, x, y):
        for point in self._points:
            if point.x() == x and point.y() == y:
                return '#'
        return ' '

    # Check if every point in the grid is touching another point in the grid
    # either horizontally, vertically or diagonally
    def all_points_touch(self):
        for point_A in self._points:

            point_is_touching = False
            for point_B in self._points:
                if point_A == point_B:
                    continue

                if point_A.is_touching(point_B):
                    point_is_touching = True

            if not point_is_touching:
                return False

        return True

    def time(self):
        return self._time

    def dim_x(self):
        x_vals = [p.x() for p in self._points]
        return max(x_vals) - min(x_vals)

    def dim_y(self):
        y_vals = [p.y() for p in self._points]
        return max(y_vals) - min(y_vals)

    def draw(self):
        x_vals = [p.x() for p in self._points]
        y_vals = [p.y() for p in self._points]

        board = ''
        for y in range(min(y_vals), max(y_vals) + 1):
            row = ''
            for x in range(min(x_vals), max(x_vals) + 1):
                row += self.char_at(x, y)

            board += row
            board += '\n'

        print board

class Point:

    def __init__(self, initial_x, initial_y, dx, dy):
        self._x = initial_x
        self._y = initial_y
        self._dx = dx
        self._dy = dy

    def x(self):
        return self._x

    def y(self):
        return self._y

    def is_touching(self, point):
        return (abs(self._y - point.y()) <= 1 and abs(self._x - point.x()) <= 1)

    def step(self):
        self._x += self._dx
        self._y += self._dy

    def __eq__(self, other):
        return (self._x == other.x()) and (self._y == other.y())

if __name__ == '__main__':
    main()
