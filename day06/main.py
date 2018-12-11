#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

import math

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    coordinate_pairs = []

    # Find the max width and height
    max_width = 1
    max_height = 1
    for coordinate_string in file_contents:
        coordinate_pair = coordinate_string.rstrip().split(", ")
        curr_coord_pair = (int(coordinate_pair[0]), int(coordinate_pair[1]))
        coordinate_pairs.append(curr_coord_pair)
        if curr_coord_pair[0] > max_width:
            max_width = curr_coord_pair[0] + 1
        if curr_coord_pair[1] > max_height:
            max_height = curr_coord_pair[1] + 1

    grid = []
    for y in range(0, max_height):
        curr_row = []
        for x in range(0, max_width):
            curr_row.append(0)
        grid.append(curr_row)

    # Plot the coordinates on the grid
    curr_coord_num = 1
    for coordinate_pair in coordinate_pairs:
        grid[coordinate_pair[1]][coordinate_pair[0]] = curr_coord_num
        curr_coord_num += 1

    # Fill in the grid based on the shortest Manhattan distances
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            curr_coord = (x, y)
            if grid[y][x] == 0:
                nearest_point = get_min_manhatten_distance(curr_coord, coordinate_pairs, grid)
                grid[y][x] = -1 * nearest_point

    # Now work out which points have infinite areas
    finite_areas = get_non_infinite_points(grid, len(coordinate_pairs))

    areas = count_points(grid)

    largest_finite_area = get_largest_finite_area(areas, finite_areas)
    print('The largest area is {area_num} with size {size}'.format(
        area_num=largest_finite_area[0],
        size=largest_finite_area[1]
    ))

def get_largest_finite_area(areas, finite_points):
    curr_largest_area = (None, 0)
    for point in finite_points:
        if areas[point] > curr_largest_area[1]:
            curr_largest_area = (point, areas[point])

    return curr_largest_area

def count_points(grid):

    areas = {}

    for row in grid:
        for cell in row:
            curr_cell_value = abs(cell)
            if curr_cell_value not in areas:
                areas[curr_cell_value] = 1
            else:
                areas[curr_cell_value] += 1

    return areas

# Work out which points have a finite area, as they are the ones who dont have a cell on the edge of the grid
def get_non_infinite_points(grid, num_points):
    finite_areas = range(1, num_points + 1)
    for y in range(0, len(grid) - 1):
        for x in range(0, len(grid[0]) - 1):
            if not (y == 0 or x == 0 or y == (len(grid) - 1) or x == (len(grid) - 1)):
                continue

            to_remove = abs(grid[y][x])
            try:
                finite_areas.remove(to_remove)
            except ValueError as ve:
                pass

    return finite_areas

# For a given coord, get the nearest point in coords from the grid using the Manhattan distance
def get_min_manhatten_distance(coord, coords, grid):

    curr_min = (None, 99999999999999999)
    is_duplicate = False

    for curr_coord in coords:
        curr_distance = get_manhatten_distance(coord, curr_coord)
        if curr_distance < curr_min[1]:
            curr_min = (curr_coord, curr_distance)
            is_duplicate = False
            continue
        if curr_distance == curr_min[1]:
            is_duplicate = True

    if is_duplicate:
        return 0

    min_point = curr_min[0]
    return grid[min_point[1]][min_point[0]]

def get_manhatten_distance(A, B):
    delta_x = abs(A[0] - B[0])
    delta_y = abs(A[1] - B[1])
    return delta_x + delta_y

def print_grid(grid, file_name=None):
    if file_name == None:
        for row in grid:
            for cell in row:
                print('{cell} '.format(
                    cell=str(cell).rjust(3)
                ), end='')
            print('\n')
    else:
        with open(file_name, 'w') as out_file:
            for row in grid:
                for cell in row:
                    out_file.write('{cell} '.format(
                        cell=str(cell).rjust(3)
                    ))
                out_file.write('\n')

if __name__ == '__main__':
  main()
