#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

import re
import ast


def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    file_contents = map(lambda l: l.rstrip(), file_contents)

    ip_declaration = file_contents[0]
    ip_reg = int(ip_declaration.split(" ")[1])

    program_contents = file_contents[1:]

    program = Program(ip_reg, program_contents)
    program.run()
    print('The value of register 0 after executing the program is {val}'.format(
        val=program.get_register_value(0)
    ))


class Program():

    def __init__(self, ip_reg, program):

        self.program = program
        self.registers = Registers([0, 0, 0, 0, 0, 0])
        self.ip_reg = ip_reg

    def run(self):

        while self.get_instruction_pointer_value() < len(self.program):

            # Load the relevant instruction, but don't execute it yet
            instruction = self.program[self.get_instruction_pointer_value()]
            op_name = instruction.split(" ")[0]
            a = int(instruction.split(" ")[1])
            b = int(instruction.split(" ")[2])
            c = int(instruction.split(" ")[3])

            # Perform the operation
            self.registers.operation(op_name, a, b, c)

            # Increment the value of the instruction pointer
            new_ip_val = self.get_instruction_pointer_value() + 1
            self.registers.set_register_value(self.ip_reg, new_ip_val)

        # Remove one from the instruction pointer, as we shouldn't have incremented it at the end
        # as the new instruction pointer value points at a non-existing instruction
        new_ip_val = self.get_instruction_pointer_value() - 1
        self.registers.set_register_value(self.ip_reg, new_ip_val)

    def get_instruction_pointer_value(self):
        return self.get_register_value(self.ip_reg)

    def get_register_value(self, reg_num):
        return self.registers.register_values()[reg_num]


class Registers():

    def __init__(self, register_values):
        self._reg_values = register_values[:]

    def register_values(self):
        return self._reg_values

    def set_register_value(self, reg_num, val):
        self._reg_values[reg_num] = val

    def get_register_value(self, reg_num):
        return self._reg_values[reg_num]

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
