#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

import re


def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    clay_locations = santitize_input(file_contents)
    r = Reservoir(clay_locations)
    r.draw('outputs/{counter}'.format(
        counter=0
    ))

    counter = 0
    resting_water_placed = 1
    while resting_water_placed > 0:
        counter += 1

        # Add some more water at the initial source
        resting_water_placed = r.add_water_unit(r.water_source)
        resting, touched = r.water_count()

    resting, touched = r.water_count()

    print('The water touches {touched} and came to rest at {resting} cells in the reservoir, for a total of {total} cells.'.format(
        touched=touched,
        resting=resting,
        total=resting+touched
    ))


def santitize_input(raw_clay_locations):
    r = '(x|y)=(\d+), [xy]=(\d+\.\.\d+)'
    matches = re.findall(r, ''.join(raw_clay_locations))

    clay_locations = []
    for match in matches:
        x_or_y = match[0]

        single_val = int(match[1])
        range_vals = match[2]
        range_from = int(range_vals.split('..')[0])
        range_to = int(range_vals.split('..')[1]) + 1
        range_list = range(range_from, range_to)

        for range_val in range_list:
            if x_or_y == "x":
                l = Location(x=single_val, y=range_val)
            else:
                l = Location(x=range_val, y=single_val)

            clay_locations.append(l)

    return clay_locations


class Reservoir():

    def __init__(self, clay_locations):
        self._generate_reservoir(clay_locations)

    def _generate_reservoir(self, clay_locations):
        r = []
        ys = map(lambda l: l.y, clay_locations)
        self.max_y = max(ys) + 1  # The deepest row that has clay
        self.min_y = min(ys)  # Need this for counting
        xs = map(lambda l: l.x, clay_locations)

        # This is the minimum and maximum values at which there is clay
        min_x = min(xs)
        max_x = max(xs)

        # Width is the largest width that we need to consider. Essentially we need to add a buffer on each side
        self.width = max_x - min_x + 3

        self.max_x = max_x - min_x + 1
        self.min_x = 0

        # Initialize the reservoir
        for y in range(self.max_y):
            row = []
            for x in range(self.width):
                row.append('.')
            r.append(row)

        # Fill in the water source.
        # Need to add it one further over than expected to account for the buffer
        r[0][501 - min_x] = '+'
        self.water_source = Location(x=501-min_x, y=0)

        # Fill in the veins of clay
        for clay_location in clay_locations:
            r[clay_location.y][clay_location.x - min_x + 1] = '#'

        self.reservoir = r

    def water_count(self):
        resting = 0
        touched = 0
        for y in range(self.max_y):
            if y < self.min_y:
                continue
            for x in range(self.width):
                l = Location(x=x, y=y)
                if self.cell_at_location(l) == '|':
                    touched += 1
                elif self.cell_at_location(l) == '~':
                    resting += 1

        return (resting, touched)

    def cell_at_location(self, location):
        if location.y < 0:
            return None

        if location.y >= self.max_y:
            return None

        if location.x < self.min_x:
            return None

        if location.x >= self.max_x + self.width:
            return None

        return self.reservoir[location.y][location.x]

    def set_cell_at_location(self, location, set_to):
        if location.y < 0:
            return None

        if location.y >= self.max_y:
            return None

        if location.x < self.min_x:
            return None

        if location.x >= self.min_x + self.width:
            return None

        self.reservoir[location.y][location.x] = set_to
        return set_to

    def cell_next_to_location(self, location, dir):
        if dir == 'l':
            new_x = location.x - 1
            new_y = location.y
        elif dir == 'r':
            new_x = location.x + 1
            new_y = location.y
        elif dir == 'd':
            new_x = location.x
            new_y = location.y + 1
        else:
            raise ValueError('Unknown direction {dir}'.format(
                dir=dir
            ))

        new_location = Location(x=new_x, y=new_y)
        return self.cell_at_location(new_location)

    def add_water_unit(self, location):
        # Copy the given started location, so we dont change it by mistake
        curr_location = Location(x=location.x, y=location.y)

        # Move down until we hit a clay or a water
        while self.cell_next_to_location(curr_location, 'd') not in ['#', '~']:
            if curr_location.y > self.max_y:
                # We reached the bottom of the map
                return 0

            curr_location.y += 1
            self.set_cell_at_location(curr_location, '|')

        # Cannot move down any more, so move to the left and right until either:
        #  a) we find a place to move down
        #  b) we cannot move left and right any more
        loc_left = Location(x=curr_location.x, y=curr_location.y)
        loc_right = Location(x=curr_location.x, y=curr_location.y)

        hit_left_wall = False
        hit_right_wall = False

        placed_resting_left = 0
        placed_resting_right = 0

        while True:
            # Move left
            loc_left = Location(x=loc_left.x - 1, y=loc_left.y)
            if self.cell_at_location(loc_left) in ['#', '~']:
                hit_left_wall = True
                break  #  We just hit a wall or reached resting water

            self.set_cell_at_location(loc_left, '|')

            # Check if we can move down at this new square
            if self.cell_next_to_location(loc_left, 'd') not in ['#', '~']:
                placed_resting_left = self.add_water_unit(loc_left)
                break

        while True:
            # Move right
            loc_right = Location(x=loc_right.x + 1, y=loc_right.y)
            if self.cell_at_location(loc_right) in ['#', '~']:
                hit_right_wall = True
                break  #  We just hit a wall or reached resting water

            self.set_cell_at_location(loc_right, '|')

            # Check if we can move down at this new square
            if self.cell_next_to_location(loc_right, 'd') not in ['#', '~']:
                placed_resting_right = self.add_water_unit(loc_right)
                break

        # If we hit walls on either side, then replace the row with resting water
        if hit_left_wall and hit_right_wall:
            y = loc_left.y
            from_x = loc_left.x + 1
            to_x = loc_right.x

            for x in range(from_x, to_x):
                l = Location(x=x, y=y)
                self.set_cell_at_location(l, '~')

            return placed_resting_left + placed_resting_right + to_x - from_x

        return placed_resting_left + placed_resting_right

    def draw(self, file_name=None):

        s = ''
        for y in range(self.max_y):
            for x in range(self.width):
                l = Location(x=x, y=y)
                cal = self.cell_at_location(l)
                s += cal
            s += '\n'

        if file_name == None:
            print(s)
        else:
            with open(file_name, 'w') as out_file:
                out_file.write(s)


class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cell = None

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)


if __name__ == '__main__':
    main()
