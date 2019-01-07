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

    stable_diff_threshold = 3

    found_stable_diff = False
    previous_diffs = [0]
    prev_sum = 0
    while not found_stable_diff:
        pl.iterate()
        new_sum = pl.sum_pot_nums_with_plants()
        new_diff = new_sum - prev_sum

        # Check that there are the correct amount of previous diffs, and that
        # they are all equal
        if len(set(previous_diffs)) == 1 and \
            len(previous_diffs) == stable_diff_threshold:

            # If they are all equal, then see if the new diff is the same too
            if new_diff == previous_diffs[0]:
                found_stable_diff = True

        previous_diffs.append(new_diff)
        prev_sum = new_sum
        if len(previous_diffs) > 3:
            del previous_diffs[0]

    print('Found a stable diff (of {diff}) after {iterations} iterations.'.format(
        diff=new_diff,
        iterations=pl.num_iterations()
    ))

    remaining_iterations = 50000000000 - pl.num_iterations()
    print('Remaining iterations: {remaining_iterations}'.format(
        remaining_iterations=remaining_iterations
    ))

    remaining_sum = remaining_iterations * new_diff
    print('{ans}'.format(
        ans=remaining_sum + pl.sum_pot_nums_with_plants()
    ))

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

    def num_iterations(self):
        return self._iteration_number

    def __str__(self):
        return self.get_state()



if __name__ == '__main__':
    main()
