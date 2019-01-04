#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    rules = []
    for line in file_contents:
        if 'initial state: ' in line:
            initial_state = line.lstrip('initial state: ').rstrip()
        elif line == '\n':
            pass
        else:
            rules.append(line.rstrip())

    pl = PotList(initial_state, rules)

    for i in range(0, 20):
        pl.iterate()

    print(pl.sum_pot_nums_with_plants())

class PotList:

    def __init__(self, initial_state, rules):
        self._padding = 1000
        self._initial_state = initial_state
        self._state = ('.' * self._padding) + self._initial_state + ('.' * self._padding)
        self._rules = rules
        self._iteration_number = 0

    def iterate(self):
        self._iteration_number += 1

        # Assume the two pots at each end remain unaffected
        new_state = self._state[:2]
        for i in range(2, len(self._state) - 2):
            pot_with_surroundings = self._state[i - 2:i + 2 + 1]
            new_state += self._iterate_pot(pot_with_surroundings)
        new_state += self._state[-2:]

        self._state = new_state


    def _iterate_pot(self, pot_with_surroundings):
        for rule in self._rules:
            rule_parts = rule.split()
            rule_in = rule_parts[0]
            rule_out = rule_parts[2]
            if rule_in == pot_with_surroundings:
                return rule_out

        # If we couldn't match one, assume it returns .
        return '.'

    def _get_pot_nums_with_plants(self):
        pot_nums = [i - self._padding for i, e in enumerate(self._state) if e == '#']
        return pot_nums

    def sum_pot_nums_with_plants(self):
        pot_nums = self._get_pot_nums_with_plants()
        return sum(pot_nums)

    def get_state(self):
        return self._state[self._padding:len(self._initial_state) + self._padding + 1]

    def __str__(self):
        return self.get_state()



if __name__ == '__main__':
    main()
