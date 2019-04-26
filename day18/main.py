#!/usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function
from enum import Enum


def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    input = map(lambda x: x.rstrip(), file_contents)

    grids = []

    grid = Grid(input)
    i = 0
    while i < 1000000000:
        grid.simulate_minute()
        curr_grid = grid.grid

        if curr_grid in grids:
            grid_index = grids.index(curr_grid)
            index_diff = i - grid_index
            full_cycles, offset = divmod(1000000000 - i, index_diff)
            grid.grid = grids[grid_index + offset - 1]
            break

        grids.append(curr_grid)
        i += 1

    print("The total resource value is {score}".format(
        score=grid.score()
    ))


class Cell(Enum):
    tree = "|"
    lumber = "#"
    open = "."


class Grid():

    def __init__(self, raw_input):
        self.grid = raw_input

    def simulate(self, num_minutes):
        for i in range(num_minutes):
            self.simulate_minute()

    def simulate_minute(self):
        new_grid = []
        for y in range(0, len(self.grid)):
            new_row = ""
            for x in range(0, len(self.grid[y])):
                new_row += self.process_cell_update(y, x)
            new_grid.append(new_row)

        self.grid = new_grid

    def process_cell_update(self, row, col):
        curr_cell = self.grid[row][col]
        adj_cells = self.adjacent_cells(row, col)
        adj_cells = "".join(adj_cells)

        num_trees = adj_cells.count(Cell.tree.value)
        num_lumber = adj_cells.count(Cell.lumber.value)
        num_open = adj_cells.count(Cell.open.value)

        new_cell = None
        if curr_cell == Cell.open.value:
            new_cell = Cell.open.value
            if num_trees >= 3:
                new_cell = Cell.tree.value

        if curr_cell == Cell.tree.value:
            new_cell = Cell.tree.value
            if num_lumber >= 3:
                new_cell = Cell.lumber.value

        if curr_cell == Cell.lumber.value:
            new_cell = Cell.open.value
            if num_lumber >= 1 and num_trees >= 1:
                new_cell = Cell.lumber.value

        return new_cell

    def adjacent_cells(self, row, col):
        cells = []
        for y in [row - 1, row, row + 1]:
            # Dont bother with rows above or below the edge of the grid
            if y < 0 or y >= len(self.grid):
                continue

            for x in [col - 1, col, col + 1]:
                # Dont include the cell itself
                if x == col and y == row:
                    continue

                # Dont bother with columns after or before the edge of the grid
                if x < 0 or x >= len(self.grid[y]):
                    continue

                # Add the cell to the adjacent cells
                cells.append(self.grid[y][x])

        return cells

    def count(self, cell_type):
        num_units = 0
        for row in self.grid:
            num_units += row.count(cell_type.value)

        return num_units

    def score(self):
        return self.count(Cell.lumber) * self.count(Cell.tree)


if __name__ == "__main__":
    main()
