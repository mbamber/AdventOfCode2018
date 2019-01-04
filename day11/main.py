#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    grid_serial_number = int(file_contents[0].rstrip())

    max_d = 300
    grid = FuelGrid(max_d, grid_serial_number)

    max_subgrid = (None, -99999999, 0)
    for d in range(0, max_d):
        print('Considering all {dimension}x{dimension} grids'.format(
            dimension=d + 1
        ))
        for y in range(0, max_d - d):
            for x in range(0, max_d - d):
                subgrid_sum = grid.summed_area_table().subgrid_sum(x + 1, y + 1, d)
                if subgrid_sum > max_subgrid[1]:
                    max_subgrid = ((x + 1, y + 1), subgrid_sum, d)

    print('The coordinates of the top left cell of the subgrid with the highest fuel value are {coordinates}.\nThe grid has total power {total_power}.\nThe grid size is {dimensions}.\nThe puzzle solution is therefore: {coordinates},{dimensions}'.format(
        coordinates='{x},{y}'.format(
            x=max_subgrid[0][0],
            y=max_subgrid[0][1]
        ),
        total_power=max_subgrid[1],
        dimensions=max_subgrid[2]
    ))

class FuelGrid():

    def __init__(self, dimension, grid_serial_number):
        self._dimension = dimension
        self._grid_serial_number = grid_serial_number

        fuel_grid = []
        for y in range(0, dimension):
            fuel_row = []
            for x in range(0, dimension):
                fuel_row.append(FuelCell(x + 1, y + 1, grid_serial_number))
            fuel_grid.append(fuel_row)

        self._fuel_grid = fuel_grid
        self._summed_area_table = Summed_Area_Table(self)

    def fuel_value_at(self, x, y):
        return (self._fuel_grid[y][x]).power_level()

    def draw(self):
        for row in self._fuel_grid:
            print(row)

    def draw_subgrid(self, min_x, min_y, d):
        for y in range(min_y - 1, min_y - 1 + d):
            for x in range(min_x - 1, min_x - 1 + d):
                print('{val} '.format(
                    val=self._fuel_grid[y][x]
                ).rjust(4), end='')
            print('')

    def summed_area_table(self):
        return self._summed_area_table

    def __len__(self):
        return self._dimension


class FuelCell():

    def __init__(self, x, y, grid_serial_number):
        self._x = x
        self._y = y
        self._grid_serial_number = grid_serial_number

    def x(self):
        return self._x

    def y(self):
        return self._y

    def grid_serial_number(self):
        return self._grid_serial_number

    def rack_id(self):
        return self.x() + 10

    def power_level(self):
        power_level = self.rack_id() * self.y()
        power_level += self.grid_serial_number()
        power_level *= self.rack_id()
        hundreds = get_place_value(power_level)
        return hundreds - 5

    def __str__(self):
        return str(self.power_level())

    def __repr__(self):
        return str(self)

class Summed_Area_Table:

    def __init__(self, grid):
        sat = []
        for y in range(0, len(grid)):
            row = []
            for x in range(0, len(grid)):
                row.append(None)
            sat.append(row)

        for y in range(0, len(grid)):
            for x in range(0, len(grid)):
                v, sat = self._get_SAT_value(sat, x, y, grid)

        self._sat = sat

    # Work out the value of the summed_area_table at the coordinate (x, y)
    def _get_SAT_value(self, sat, x, y, grid):
        curr_cell = grid.fuel_value_at(x - 1, y - 1)

        if x == 0:
            if y == 0:
                v = curr_cell

            else:
                v = curr_cell + sat[y - 1][x]

        else:
            if y == 0:
                v = curr_cell + sat[y][x - 1]

            else:
                v = curr_cell - sat[y - 1][x - 1] + sat[y][x - 1] + sat[y - 1][x]

        sat[y][x] = v
        return v, sat

    def subgrid_sum(self, min_x, min_y, d):
        return self._sat[min_y - 1][min_x - 1] + \
            self._sat[min_y - 1 + d][min_x - 1 + d] - \
            self._sat[min_y - 1 + d][min_x - 1] - \
            self._sat[min_y - 1][min_x - 1 + d]

    def draw(self):
        for row in self._sat:
            print(row)

    def draw_subgrid(self, min_x, min_y, d):
        for y in range(min_y - 1, min_y - 1 + d):
            for x in range(min_x - 1, min_x - 1 + d):
                print('{val} '.format(
                    val=self._sat[y][x]
                ).rjust(4), end='')
            print('')

# Get the place value of num, as position place_num. i.e. get_place_value(x, 0)
# will find the value of the units of x, and get_place_value(x, 2) will find the
# value of the hundreds of x
def get_place_value(num, place_num=2):
    num = abs(num)
    num_str = str(num)
    place_vals = num_str[::-1]
    if len(place_vals) <= place_num:
        return 0
    else:
        return int(place_vals[place_num])

if __name__ == '__main__':
    main()
