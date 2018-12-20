#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    grid_serial_number = int(file_contents[0].rstrip())

    grid = FuelGrid(300, grid_serial_number)
    subgrid = grid.subgrid_with_highest_fuel_value()
    print 'The coordinates of the top left cell of the subgrid with the highest fuel value are {coordinates}.\nThe subgrid has total fuel value {fuel_value}'.format(
        coordinates='{x},{y}'.format(
            x=subgrid[0][0],
            y=subgrid[0][1]
        ),
        fuel_value=subgrid[1]
    )

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

    def subgrid_with_highest_fuel_value(self, dimension=3):
        highest = (None, -5*dimension*dimension - 1)
        for y in range(0, self._dimension - dimension):
            for x in range(0, self._dimension - dimension):
                fuel_value = self._sum_fuel_value(x, y, dimension)
                if fuel_value > highest[1]:
                    highest = ((x+1, y+1), fuel_value)

        return highest

    def _sum_fuel_value(self, x, y, dimension):
        total = 0
        for y_2 in range(y, y + dimension):
            for x_2 in range(x, x + dimension):
                total += self._fuel_value_at(x_2, y_2)

        return total

    def _fuel_value_at(self, x, y):
        return (self._fuel_grid[y][x]).power_level()

    def draw(self):
        for row in self._fuel_grid:
            print row

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
