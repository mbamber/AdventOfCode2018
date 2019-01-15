#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

import re
import ast

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    prev_line = None

    captured_output = []
    test_program = []

    captured_output_regex = 'Before:\s+(?P<before>\[\d+, \d+, \d+, \d+\])\n(?P<op>\d+ \d+ \d+ \d+)\nAfter:\s+(?P<after>\[\d+, \d+, \d+, \d+\])'
    test_regex = '(?P<test>\d+ \d+ \d+ \d+)(?!\nAfter)'

    raw_captured_output = re.findall(captured_output_regex, ''.join(file_contents))
    raw_test_program = re.findall(test_regex, ''.join(file_contents))

    # print(raw_captured_output)
    captured_output = map(lambda (x, y, z): (ast.literal_eval(x), map(int, y.split()), ast.literal_eval(z)), raw_captured_output)
    test_program = map(lambda x: map(int, x.split()), raw_test_program)

    # print(captured_output[-3])

    # return

    # Go through each set of inputs in the input and work out which ones could
    # be at least three different opcodes
    num_at_least_3 = 0

    for (before, op, after) in captured_output:
        possible_ops = 0

        op_code = op[0]
        a = op[1]
        b = op[2]
        c = op[3]

        r = Registers(before)
        r.addr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.mulr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.muli(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.banr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.bani(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.borr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.bori(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.setr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.seti(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.gtri(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.gtir(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.gtrr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.eqri(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.eqir(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        r = Registers(before)
        r.eqrr(a, b, c)
        if r.register_values() == after:
            possible_ops += 1

        if possible_ops >= 3:
            num_at_least_3 += 1
            print('Input: {before}, {op}, {after} behaved like three or more opcodes'.format(
                before=before,
                op=op,
                after=after
            ))
        else:
            print('Input: {before}, {op}, {after} DID NOT behave like three or more opcodes'.format(
                before=before,
                op=op,
                after=after
            ))

    print('There are {counter} inputs which behave like three or more opcodes.'.format(
        counter=num_at_least_3
    ))


class Registers():

    def __init__(self, register_values):
        self._reg_values = register_values[:]

    def register_values(self):
        return self._reg_values

    def addr(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] + self._reg_values[b]

    def addi(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] + b

    def mulr(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] * self._reg_values[b]

    def muli(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] * b

    def banr(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] & self._reg_values[b]

    def bani(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] & b

    def borr(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] | self._reg_values[b]

    def bori(self, a, b, c):
        self._reg_values[c] = self._reg_values[a] | b

    def setr(self, a, b, c):
        self._reg_values[c] = self._reg_values[a]

    def seti(self, a, b, c):
        self._reg_values[c] = a

    def gtir(self, a, b, c):
        self._reg_values[c] = 1 if a > self._reg_values[b] else 0

    def gtri(self, a, b, c):
        self._reg_values[c] = 1 if self._reg_values[a] > b else 0

    def gtrr(self, a, b, c):
        self._reg_values[c] = 1 if self._reg_values[a] > self._reg_values[b] else 0

    def eqir(self, a, b, c):
        self._reg_values[c] = 1 if a == self._reg_values[b] else 0

    def eqri(self, a, b, c):
        self._reg_values[c] = 1 if self._reg_values[a] == b else 0

    def eqrr(self, a, b, c):
        self._reg_values[c] = 1 if self._reg_values[a] == self._reg_values[b] else 0


if __name__ == '__main__':
    main()
