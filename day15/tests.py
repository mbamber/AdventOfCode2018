#! /usr/bin
# -*- coding: UTF-8 -*-
from __future__ import print_function

import unittest
import datetime
import logging
import sys

from main import Cavern, Unit, Elf, Goblin, Point, PathStep, UnitDiedException


class TestUnitOrdering(unittest.TestCase):

    def setUp(self):
        # The test map is given below:
        #
        #                 1111
        #       01234567890123
        #     0 ##############
        #     1 #G.#E#.###.#.#
        #     2 #..#.#...#####
        #     3 ##...#E#.#.G.#
        #     4 ####.....#####
        #     5 ##############
        self.movement_cavern = Cavern([
            '##############',
            '#G.#E#.###.#.#',
            '#..#.#...#####',
            '##...#E#.#.G.#',
            '####.....#####',
            '##############'
        ])
        # Manually change the units, so the elves are in the wrong order
        logging.debug(self.movement_cavern.alive_elves())
        self.movement_cavern.alive_elves()[0].loc.y = 4
        self.assertEqual(self.movement_cavern.alive_elves()[0].loc.y, 4)

        # The test map is given below:
        #
        #                 1111
        #       01234567890123
        #     0 ##############
        #     1 #GE#.#.###.#.#
        #     2 #E.#.#...#####
        #     3 ##...#.#.#...#
        #     4 ####.....#####
        #     5 ##############
        self.attack_cavern = Cavern([
            '##############',
            '#GE#.#.###.#.#',
            '#E.#.#...#####',
            '##...#.#.#...#',
            '####.....#####',
            '##############'
        ])

    def test_order_by_location(self):
        # Kill all the goblins
        for u in self.movement_cavern.alive_goblins():
            u.hp = 0

        elves = self.movement_cavern.alive_elves()
        units = self.movement_cavern.order_units_by_position(elves)

        self.assertEqual(units[0].loc.x, 6)
        self.assertEqual(units[0].loc.y, 3)
        self.assertEqual(units[1].loc.x, 4)
        self.assertEqual(units[1].loc.y, 4)

    def test_order_with_different_types(self):
        elves = self.movement_cavern.alive_elves()
        units = self.movement_cavern.order_units_by_position(elves)

        self.assertEqual(units[0].loc.x, 6)
        self.assertEqual(units[0].loc.y, 3)
        self.assertEqual(units[1].loc.x, 4)
        self.assertEqual(units[1].loc.y, 4)

    def test_attack_order_by_hit_points(self):
        # Set one of the units to a lower hit points
        self.attack_cavern.alive_elves()[1].hp = 1

        elves = self.attack_cavern.alive_elves()
        units = self.attack_cavern.order_units_by_hit_points(elves)
        self.assertEqual(units[0].loc.x, 1)
        self.assertEqual(units[0].loc.y, 2)
        self.assertEqual(units[1].loc.x, 2)
        self.assertEqual(units[1].loc.y, 1)

    def test_attack_order_by_location(self):
        elves = self.attack_cavern.alive_elves()
        units = self.attack_cavern.order_units_by_hit_points(elves)
        self.assertEqual(units[0].loc.x, 2)
        self.assertEqual(units[0].loc.y, 1)
        self.assertEqual(units[1].loc.x, 1)
        self.assertEqual(units[1].loc.y, 2)


class TestUnitTurns(unittest.TestCase):

    def setUp(self):
        # The test map is given below:
        #
        #                 1111
        #       01234567890123
        #     0 ##############
        #     1 #G.#E#.###.#.#
        #     2 #..#.#..E#####
        #     3 ##...#E#.#.G.#
        #     4 ####...G.#####
        #     5 ##############
        self.cavern_1 = Cavern([
            '##############',
            '#G.#E#.###.#.#',
            '#..#.#..E#####',
            '##...#E#.#.G.#',
            '####...G.#####',
            '##############'
        ])

        # The test map is given below:
        #
        #       012345
        #     0 ######
        #     1 #...G#
        #     2 #....#
        #     3 #....#
        #     4 #G..E#
        #     5 ######
        self.cavern_2 = Cavern([
            '######',
            '#...G#',
            '#....#',
            '#....#',
            '#G..E#',
            '######'
        ])

        self.cavern_custom = Cavern([
            '##############',
            '#G.#E#.###.#.#',
            '#..#.#..E#####',
            '##...#E#.#...#',
            '####...G.#####',
            '##############'
        ])

    def test_full_round(self):
        self.cavern_1.step(1)

        # Check all the units moved correctly
        self.assertIsNone(self.cavern_1.unit_at(Point(1, 1)))
        self.assertTrue(type(self.cavern_1.unit_at(Point(2, 1))) == Goblin)
        self.assertIsNone(self.cavern_1.unit_at(Point(4, 1)))
        self.assertTrue(type(self.cavern_1.unit_at(Point(4, 2))) == Elf)
        self.assertIsNone(self.cavern_1.unit_at(Point(8, 2)))
        self.assertTrue(type(self.cavern_1.unit_at(Point(8, 3))) == Elf)
        self.assertIsNone(self.cavern_1.unit_at(Point(6, 3)))
        self.assertTrue(type(self.cavern_1.unit_at(Point(6, 4))) == Elf)
        self.assertTrue(type(self.cavern_1.unit_at(Point(11, 3))) == Goblin)
        self.assertTrue(type(self.cavern_1.unit_at(Point(7, 4))) == Goblin)

        # Now check that all the units apart from the ones at (6, 4) and (7, 4) have 200 HP
        self.assertTrue(self.cavern_1.unit_at(Point(2, 1)).hp == 200)
        self.assertTrue(self.cavern_1.unit_at(Point(4, 2)).hp == 200)
        self.assertTrue(self.cavern_1.unit_at(Point(8, 3)).hp == 200)
        self.assertTrue(self.cavern_1.unit_at(Point(6, 4)).hp == 197)
        self.assertTrue(self.cavern_1.unit_at(Point(11, 3)).hp == 200)
        self.assertTrue(self.cavern_1.unit_at(Point(7, 4)).hp == 197)

    def test_full_round_equal_distance(self):
        self.cavern_2.step(1)

        # Check all the units moved correctly
        self.assertIsNone(self.cavern_2.unit_at(Point(4, 1)))
        self.assertTrue(type(self.cavern_2.unit_at(Point(4, 2))) == Goblin)
        self.assertIsNone(self.cavern_2.unit_at(Point(1, 4)))
        self.assertTrue(type(self.cavern_2.unit_at(Point(2, 4))) == Goblin)
        self.assertIsNone(self.cavern_2.unit_at(Point(4, 4)))
        self.assertTrue(type(self.cavern_2.unit_at(Point(4, 3))) == Elf)

        # Now check that all the units (apart from the first Goblin) have 200 HP
        self.assertTrue(self.cavern_2.unit_at(Point(4, 2)).hp == 197)
        self.assertTrue(self.cavern_2.unit_at(Point(2, 4)).hp == 200)
        self.assertTrue(self.cavern_2.unit_at(Point(4, 3)).hp == 200)

    def test_full_game_custom(self):
        rounds_played, hp, winning_team = self.cavern_custom.play()

        self.assertEqual(rounds_played, 68)
        self.assertEqual(hp, 300)
        self.assertEqual(winning_team, Elf)

    def test_examples(self):
        example_caverns = [
            {
                "starting_cavern": [
                    "#######",
                    "#G..#E#",
                    "#E#E.E#",
                    "#G.##.#",
                    "#...#E#",
                    "#...E.#",
                    "#######"
                ],
                "rounds_played": 37,
                "remaining_hit_points": 982,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#######",
                    "#E..EG#",
                    "#.#G.E#",
                    "#E.##E#",
                    "#G..#.#",
                    "#..E#.#",
                    "#######"
                ],
                "rounds_played": 46,
                "remaining_hit_points": 859,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#######",
                    "#E.G#.#",
                    "#.#G..#",
                    "#G.#.G#",
                    "#G..#.#",
                    "#...E.#",
                    "#######"
                ],
                "rounds_played": 35,
                "remaining_hit_points": 793,
                "winning_team": Goblin
            },
            {
                "starting_cavern": [
                    "#######",
                    "#.E...#",
                    "#.#..G#",
                    "#.###.#",
                    "#E#G#G#",
                    "#...#G#",
                    "#######"
                ],
                "rounds_played": 54,
                "remaining_hit_points": 536,
                "winning_team": Goblin
            },
            {
                "starting_cavern": [
                    "#########",
                    "#G......#",
                    "#.E.#...#",
                    "#..##..G#",
                    "#...##..#",
                    "#...#...#",
                    "#.G...G.#",
                    "#.....G.#",
                    "#########"
                ],
                "rounds_played": 20,
                "remaining_hit_points": 937,
                "winning_team": Goblin
            },

        ]

        for test_data in example_caverns:
            rounds_played, hp, winning_team = Cavern(
                test_data["starting_cavern"]).play()
            self.assertEqual(rounds_played, test_data["rounds_played"])
            self.assertEqual(hp, test_data["remaining_hit_points"])
            self.assertEqual(winning_team, test_data["winning_team"])


class TestLocationsAreAdjacent(unittest.TestCase):

    def test_adjacent_x_location(self):
        loc_1 = Point(0, 0)
        loc_2 = Point(1, 0)
        self.assertTrue(loc_1.is_adjacent_to(loc_2))

    def test_adjacent_x_location_reverse(self):
        loc_1 = Point(1, 0)
        loc_2 = Point(0, 0)
        self.assertTrue(loc_1.is_adjacent_to(loc_2))

    def test_adjacent_y_location(self):
        loc_1 = Point(0, 0)
        loc_2 = Point(0, 1)
        self.assertTrue(loc_1.is_adjacent_to(loc_2))
        self.assertTrue(loc_2.is_adjacent_to(loc_1))

    def test_diagonal_location(self):
        loc_1 = Point(0, 0)
        loc_2 = Point(1, 1)
        self.assertFalse(loc_1.is_adjacent_to(loc_2))

    def test_far_x_location(self):
        loc_1 = Point(0, 0)
        loc_2 = Point(2, 0)
        self.assertFalse(loc_1.is_adjacent_to(loc_2))

    def test_far_y_location(self):
        loc_1 = Point(0, 0)
        loc_2 = Point(0, 2)
        self.assertFalse(loc_1.is_adjacent_to(loc_2))


class TestPathFinding(unittest.TestCase):

    def setUp(self):
        # The test map is given below:
        #
        #                 1111
        #       01234567890123
        #     0 ##############
        #     1 #G.#E#.###.#.#
        #     2 #..#.#...#####
        #     3 ##...#E#.#.G.#
        #     4 ####.....#####
        #     5 ##############
        #     6 #...##########
        #     7 ##..##########
        #     8 ##...#########
        #     9 ##############

        self.cavern = Cavern([
            '##############',
            '#G.#E#.###.#.#',
            '#..#.#...#####',
            '##...#E#.#.G.#',
            '####.....#####',
            '##############',
            '#...##########',
            '##..##########',
            '##...#########',
            '##############'
        ])

    def test_path_starts_on_wall(self):
        shortest_path = self.cavern.path_length(Point(2, 0), Point(2, 1))
        expected_result = None
        self.assertEqual(shortest_path, expected_result)

    def test_path_ends_on_wall(self):
        shortest_path = self.cavern.path_length(Point(2, 1), Point(2, 0))
        expected_result = None
        self.assertEqual(shortest_path, expected_result)

    def test_path_starts_on_unit(self):
        shortest_path = self.cavern.path_length(Point(1, 1), Point(1, 2))
        expected_result = PathStep(0, Point(1, 2))
        self.assertEqual(shortest_path, expected_result)

    def test_path_ends_on_unit(self):
        shortest_path = self.cavern.path_length(Point(1, 2), Point(1, 1))
        expected_result = PathStep(0, Point(1, 1))
        self.assertEqual(shortest_path, expected_result)

    def test_path_unreachable_because_wall(self):
        shortest_path = self.cavern.path_length(Point(10, 1), Point(12, 1))
        expected_result = None
        self.assertEqual(shortest_path, expected_result)

    def test_path_unreachable_because_unit(self):
        shortest_path = self.cavern.path_length(Point(10, 3), Point(12, 3))
        expected_result = None
        self.assertEqual(shortest_path, expected_result)

    def test_empty_path(self):
        shortest_path = self.cavern.path_length(Point(2, 3), Point(4, 2))
        expected_result = PathStep(2, Point(3, 3))
        self.assertEqual(shortest_path, expected_result)

    def test_valid_route_with_two_paths(self):
        shortest_path = self.cavern.path_length(Point(1, 1), Point(4, 1))
        expected_result = PathStep(6, Point(2, 1))
        self.assertEqual(shortest_path, expected_result)

    def test_path_with_unit_obstruction(self):
        shortest_path = self.cavern.path_length(Point(6, 2), Point(6, 4))
        expected_result = PathStep(5, Point(7, 2))
        self.assertEqual(shortest_path, expected_result)

    def test_path_with_overlapping_paths(self):
        shortest_path_forward = self.cavern.path_length(
            Point(1, 6), Point(4, 8))
        expected_result_forward = PathStep(4, Point(2, 6))
        shortest_path_backward = self.cavern.path_length(
            Point(4, 8), Point(1, 6))
        expected_result_backward = PathStep(4, Point(3, 8))

        self.assertEqual(shortest_path_forward, expected_result_forward)
        self.assertEqual(shortest_path_backward, expected_result_backward)


class TestPerformance(unittest.TestCase):

    def setUp(self):
        # The test map is given below:
        #
        #                 1111111111222222222233333333334444444444555555
        #       01234567890123456789012345678901234567890123456789012345
        #     0 ########################################################
        #     1 #......................................................#
        #     2 #......................................................#
        #     3 #......................................................#
        #     4 #......................................................#
        #     5 ########################################################

        self.cavern = Cavern([
            '########################################################',
            '#......................................................#',
            '#......................................................#',
            '#......................................................#',
            '#......................................................#',
            '########################################################'
        ])

    def test_long_path(self):
        start_time = datetime.datetime.now()
        shortest_path = self.cavern.path_length(Point(2, 2), Point(53, 3))
        end_time = datetime.datetime.now()

        expected_result = PathStep(51, Point(3, 2))
        self.assertEqual(shortest_path, expected_result)

        running_time = (end_time - start_time).total_seconds()
        time_threshold_seconds = 1
        self.assertTrue(running_time <= time_threshold_seconds,
                        msg="Test did not complete in a reasonable time ({threshold} seconds). {elapsed} seconds elapsed.".format(
                            threshold=time_threshold_seconds,
                            elapsed=running_time
                        ))


class TestElfDeath(unittest.TestCase):

    def setUp(self):
        pass

    # Same examples as earlier
    def test_examples(self):
        example_caverns = [
            {
                "starting_cavern": [
                    "#######",
                    "#.G...#",
                    "#...EG#",
                    "#.#.#G#",
                    "#..G#E#",
                    "#.....#",
                    "#######"
                ],
                "elf_attack": 15,
                "rounds_played": 29,
                "remaining_hit_points": 172,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#######",
                    "#E..EG#",
                    "#.#G.E#",
                    "#E.##E#",
                    "#G..#.#",
                    "#..E#.#",
                    "#######"
                ],
                "elf_attack": 4,
                "rounds_played": 33,
                "remaining_hit_points": 948,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#######",
                    "#E.G#.#",
                    "#.#G..#",
                    "#G.#.G#",
                    "#G..#.#",
                    "#...E.#",
                    "#######"
                ],
                "elf_attack": 15,
                "rounds_played": 37,
                "remaining_hit_points": 94,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#######",
                    "#.E...#",
                    "#.#..G#",
                    "#.###.#",
                    "#E#G#G#",
                    "#...#G#",
                    "#######"
                ],
                "elf_attack": 12,
                "rounds_played": 39,
                "remaining_hit_points": 166,
                "winning_team": Elf
            },
            {
                "starting_cavern": [
                    "#########",
                    "#G......#",
                    "#.E.#...#",
                    "#..##..G#",
                    "#...##..#",
                    "#...#...#",
                    "#.G...G.#",
                    "#.....G.#",
                    "#########"
                ],
                "elf_attack": 34,
                "rounds_played": 30,
                "remaining_hit_points": 38,
                "winning_team": Elf
            },

        ]

        for test_data in example_caverns:
            cavern = Cavern(
                test_data["starting_cavern"], elf_attack=test_data["elf_attack"], ignore_elf_death=False)
            try:
                turns, hp, winning_team = cavern.play()
            except UnitDiedException as ude:
                self.fail("An elf died unexpectedly ({elf})".format(
                    elf=ude.unit.debug_str()
                ))

            self.assertEqual(turns, test_data["rounds_played"])
            self.assertEqual(hp, test_data["remaining_hit_points"])
            self.assertEqual(winning_team, test_data["winning_team"])


def enable_logging():
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.handlers = []
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    unittest.main()
