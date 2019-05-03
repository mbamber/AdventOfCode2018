#! /usr/bin
# -*- coding: UTF-8 -*-

from main import Registers, Program
import unittest


class TestRegisterOperations(unittest.TestCase):

    def setUp(self):
        self.r = Registers([2, 5, 7, 9])

    def test_addr(self):
        self.r.addr(0, 1, 3)
        expected_output = [2, 5, 7, 7]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_addi(self):
        self.r.addi(0, 1, 3)
        expected_output = [2, 5, 7, 3]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_mulr(self):
        self.r.mulr(0, 2, 3)
        expected_output = [2, 5, 7, 14]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_muli(self):
        self.r.muli(0, 1, 3)
        expected_output = [2, 5, 7, 2]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_banr(self):
        self.r.banr(0, 1, 3)
        expected_output = [2, 5, 7, 0]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_bani(self):
        self.r.bani(1, 1, 3)
        expected_output = [2, 5, 7, 1]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_borr(self):
        self.r.borr(0, 1, 3)
        expected_output = [2, 5, 7, 7]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_bori(self):
        self.r.bori(0, 8, 3)
        expected_output = [2, 5, 7, 10]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_setr(self):
        self.r.setr(0, 1, 3)
        expected_output = [2, 5, 7, 2]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_seti(self):
        self.r.seti(0, 1, 3)
        expected_output = [2, 5, 7, 0]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_gtir(self):
        self.r.gtir(6, 1, 3)
        expected_output = [2, 5, 7, 1]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_gtri(self):
        self.r.gtri(1, 6, 3)
        expected_output = [2, 5, 7, 0]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_gtrr(self):
        self.r.gtrr(2, 1, 3)
        expected_output = [2, 5, 7, 1]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_eqir(self):
        self.r.eqir(5, 1, 3)
        expected_output = [2, 5, 7, 1]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_eqri(self):
        self.r.eqri(0, 1, 3)
        expected_output = [2, 5, 7, 0]
        self.assertEqual(self.r.register_values(), expected_output)

    def test_eqrr(self):
        self.r.eqrr(0, 1, 3)
        expected_output = [2, 5, 7, 0]
        self.assertEqual(self.r.register_values(), expected_output)


class TestProgram(unittest.TestCase):

    def test_example_program(self):

        ip_reg = 0
        program_contents = [
            "seti 5 0 1",
            "seti 6 0 2",
            "addi 0 1 0",
            "addr 1 2 3",
            "setr 1 0 0",
            "seti 8 0 4",
            "seti 9 0 5"
        ]

        program = Program(ip_reg, program_contents)
        program.run()

        self.assertEqual(program.get_register_value(0), 6)
        self.assertEqual(program.get_register_value(1), 5)
        self.assertEqual(program.get_register_value(2), 6)
        self.assertEqual(program.get_register_value(3), 0)
        self.assertEqual(program.get_register_value(4), 0)
        self.assertEqual(program.get_register_value(5), 9)


if __name__ == '__main__':
    unittest.main()
