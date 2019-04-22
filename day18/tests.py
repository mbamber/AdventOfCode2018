#!/usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function
import unittest
from main import Grid

class TestExamples(unittest.TestCase):

    def setUp(self):
        pass

    def test_example(self):
        example = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

        g = Grid(example.split("\n"))
        g.simulate(10)
        self.assertEqual(g.score(), 1147)

if __name__ == '__main__':
    unittest.main()
