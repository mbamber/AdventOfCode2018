#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

import math

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    threshold = 10000

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

    coords_less_than_threshold = []

    # Loop through each point, and record which coordinates have a total manhatten
    # distance less than the threshold
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            curr_coord = (x, y)
            curr_total = 0
            for coord in coordinate_pairs:
                curr_total += get_manhatten_distance(coord, curr_coord)
            if curr_total < threshold:
                coords_less_than_threshold.append(curr_coord)

    print('The size of the area with total manhatten distance less than {threshold} is {size}'.format(
        threshold=threshold,
        size=len(coords_less_than_threshold)
    ))

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
