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

    inputs_by_opcode = {}

    # Group the inputs by op_code
    for (before, op, after) in captured_output:
        op_code = op[0]

        if op_code in inputs_by_opcode:
            inputs_by_opcode[op_code].append((before, op, after))
        else:
            inputs_by_opcode[op_code] = [(before, op, after)]

    op_mapping = {}

    # Go through each op code, and determine the possible operations that it could be
    for op_code in range(0, 16):
        op_possibles = []
        for op_tuple in inputs_by_opcode[op_code]:
            before = op_tuple[0]
            op = op_tuple[1]
            after = op_tuple[2]

            a = op[1]
            b = op[2]
            c = op[3]

            # build a set of all the possible operation names that this could be
            possibles = set()

            r = Registers(before)
            r.addi(a, b, c)
            if r.register_values() == after:
                possibles.add('addi')

            r = Registers(before)
            r.addr(a, b, c)
            if r.register_values() == after:
                possibles.add('addr')

            r = Registers(before)
            r.muli(a, b, c)
            if r.register_values() == after:
                possibles.add('muli')

            r = Registers(before)
            r.mulr(a, b, c)
            if r.register_values() == after:
                possibles.add('mulr')

            r = Registers(before)
            r.borr(a, b, c)
            if r.register_values() == after:
                possibles.add('borr')

            r = Registers(before)
            r.bori(a, b, c)
            if r.register_values() == after:
                possibles.add('bori')

            r = Registers(before)
            r.banr(a, b, c)
            if r.register_values() == after:
                possibles.add('banr')

            r = Registers(before)
            r.bani(a, b, c)
            if r.register_values() == after:
                possibles.add('bani')

            r = Registers(before)
            r.seti(a, b, c)
            if r.register_values() == after:
                possibles.add('seti')

            r = Registers(before)
            r.setr(a, b, c)
            if r.register_values() == after:
                possibles.add('setr')

            r = Registers(before)
            r.gtir(a, b, c)
            if r.register_values() == after:
                possibles.add('gtir')

            r = Registers(before)
            r.gtri(a, b, c)
            if r.register_values() == after:
                possibles.add('gtri')

            r = Registers(before)
            r.gtrr(a, b, c)
            if r.register_values() == after:
                possibles.add('gtrr')

            r = Registers(before)
            r.eqir(a, b, c)
            if r.register_values() == after:
                possibles.add('eqir')

            r = Registers(before)
            r.eqri(a, b, c)
            if r.register_values() == after:
                possibles.add('eqri')

            r = Registers(before)
            r.eqrr(a, b, c)
            if r.register_values() == after:
                possibles.add('eqrr')

            op_possibles.append(possibles)

        commons = set.intersection(*op_possibles)
        op_mapping[op_code] = commons

    # Work out what op code maps to what operation
    final_op_mapping = {}
    while not len(op_mapping) == 0:
        for op_code in range(0, 16):
            if op_code not in op_mapping:
                continue
            possible_ops = op_mapping[op_code]
            if len(possible_ops) == 1:
                operation = possible_ops.pop()
                final_op_mapping[op_code] = operation

                # Discard this operation from all other sets
                map(lambda poss_ops: poss_ops.discard(operation), op_mapping.values())

            # If there are no mpre possible operations for this op_code,
            # then remove it
            if len(possible_ops) == 0:
                op_mapping.pop(op_code)

    # Run the test program
    r = Registers([0, 0, 0, 0])
    for test_line in test_program:
        op_code = test_line[0]
        a = test_line[1]
        b = test_line[2]
        c = test_line[3]

        op_name = final_op_mapping[op_code]
        r.operation(op_name, a, b, c)

    final_registers = r.register_values()
    print('The value of register 0 after executing the test program is {val}'.format(
        val=final_registers[0]
    ))




class Registers():

    def __init__(self, register_values):
        self._reg_values = register_values[:]

    def register_values(self):
        return self._reg_values

    def operation(self, op_name, a, b, c):
        if op_name == 'addr':
            self.addr(a, b, c)
        if op_name == 'addi':
            self.addi(a, b, c)
        if op_name == 'mulr':
            self.mulr(a, b, c)
        if op_name == 'muli':
            self.muli(a, b, c)
        if op_name == 'banr':
            self.banr(a, b, c)
        if op_name == 'bani':
            self.bani(a, b, c)
        if op_name == 'borr':
            self.borr(a, b, c)
        if op_name == 'bori':
            self.bori(a, b, c)
        if op_name == 'setr':
            self.setr(a, b, c)
        if op_name == 'seti':
            self.seti(a, b, c)
        if op_name == 'gtir':
            self.gtir(a, b, c)
        if op_name == 'gtri':
            self.gtri(a, b, c)
        if op_name == 'gtrr':
            self.gtrr(a, b, c)
        if op_name == 'eqir':
            self.eqir(a, b, c)
        if op_name == 'eqri':
            self.eqri(a, b, c)
        if op_name == 'eqrr':
            self.eqrr(a, b, c)

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
