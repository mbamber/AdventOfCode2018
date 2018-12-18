#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    num_players = int(file_contents[0].rstrip().split('; ')[0].split(' ')[0])
    final_marble_points = int(file_contents[0].rstrip().split('; ')[1].split(' ')[4])

    # Initialize the scoreboard
    scoreboard = {}
    for p_num in range(1, num_players + 1):
        scoreboard[p_num] = 0

    circle = Circle(0)

    curr_marble_points = 0
    curr_marble_val = 1
    curr_player = 1
    while not curr_marble_val == final_marble_points:
        if curr_marble_val % 23 == 0:
            removed_val = circle.remove(7)
            curr_marble_points = removed_val + curr_marble_val
            scoreboard[curr_player] += curr_marble_points

        else:
            circle.insert(curr_marble_val, 2)

        curr_marble_val += 1

        curr_player += 1
        if curr_player > num_players:
            curr_player = 1

    print('The winning score is {winning_score}'.format(
        winning_score=max(scoreboard.values())
    ))

# A circular list
class Circle(object):

    def __init__(self, initial_element):
        self._elements = [initial_element]
        self._current_element_index = 0

    def current_element(self):
        return self._elements[self._current_element_index]

    # Insert value into the circle, position places after the current element
    # set_current_element determines if the current element should be updated
    # to the new inserted position
    def insert(self, value, position=2, set_current_element=True):
        # Sanity check the position
        if position <= 0:
            raise ValueError('Position {position} cannot be less than 1!'.format(
                position=position
            ))

        index = self._current_element_index + position
        if index > len(self._elements):
            index = index - len(self._elements)

        if set_current_element:
            self._current_element_index = index

        self._elements.insert(index, value)

    # Remove the element position counter clockwise from the current element
    # set_current_element determines if the current element should be updated
    # to the element directly clockwise from the removed element
    def remove(self, position=7, set_current_element=True):
        if position <= 0:
            raise ValueError('Position {position} cannot be less than 1!'.format(
                position=position
            ))

        index = (self._current_element_index - position) % len(self._elements)

        e = self._elements.pop(index)

        if set_current_element:
            if index == len(self._elements):
                index = 0
            self._current_element_index = index

        return e

    def __str__(self):
        str_elems = self._elements[:]
        str_elems[self._current_element_index] = '({val})'.format(val=self.current_element())
        return str(str_elems)

if __name__ == '__main__':
    main()
