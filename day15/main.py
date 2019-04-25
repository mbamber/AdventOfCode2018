#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function
import logging
import sys


def main():

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(levelname)s :: %(message)s')

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    raw_cavern = map(lambda x: x.rstrip(), file_contents)
    cavern = Cavern(raw_cavern)

    turns, hp, winning_team = cavern.play()

    print(turns, hp, winning_team)
    print(turns * hp)


class Cavern():

    def __init__(self, raw_cavern):
        self.cavern, self.all_units = self._generate_cavern(raw_cavern)

    def units(self, t):
        return filter(lambda u: type(u) == t, self.all_units)

    def alive_elves(self):
        return [u for u in self.units(Elf) if u.is_alive()]

    def alive_goblins(self):
        return [u for u in self.units(Goblin) if u.is_alive()]

    # Generate the cavern in an easy to process way
    def _generate_cavern(self, raw_cavern):
        cavern = []
        units = []

        for y in range(0, len(raw_cavern)):
            row = []
            for x in range(0, len(raw_cavern[y])):
                cavern_tile = raw_cavern[y][x]
                if cavern_tile == 'G':
                    row.append('.')
                    units.append(Goblin(Point(x, y)))
                elif cavern_tile == 'E':
                    row.append('.')
                    units.append(Elf(Point(x, y)))
                else:
                    row.append(cavern_tile)

            cavern.append(row)

        return cavern, units

    # Order the units ready for moving
    def order_units_by_position(self, units):

        # Sort by their location, in reading order
        sorted_units = sorted(units, key=lambda unit: unit.loc)
        return sorted_units

    # Order the units for attacking
    def order_units_by_hit_points(self, units):

        # Sort by hit points, and break ties using the location.
        # Note, python sorting is stable, so things that have a tie break remain
        # in the same order as they were. This means we can sort by the most
        # specific stuff first (the location), and then work our way up to the
        # most general sort (the hit_points)
        sorted_units = self.order_units_by_position(units)
        sorted_units = sorted(sorted_units, key=lambda unit: unit.hp)
        return sorted_units

    def cavern_tile_at(self, loc):
        if loc.y >= len(self.cavern) or loc.x >= len(self.cavern[loc.y]):
            raise ValueError('Invalid coordinates {p} for cavern'.format(
                p=loc
            ))
        return self.cavern[loc.y][loc.x]

    def unit_at(self, loc):
        # Create a list of all the alive units at the coordinate pair. The list
        # will either be empty, or will have exactly one element
        units_at_loc = [
            unit for unit in self.all_units if unit.loc == loc and unit.is_alive()]

        if len(units_at_loc) == 0:
            return None
        else:
            return units_at_loc[0]

    def draw(self, filename=None):

        if filename is None:
            for y in range(0, len(self.cavern)):
                for x in range(0, len(self.cavern[y])):
                    p = Point(x, y)
                    unit = self.unit_at(p)
                    if unit is None:
                        print(self.cavern_tile_at(p), end='')
                    else:
                        print(unit, end='')
                print('')
        else:
            with open(filename, "w") as f:
                for y in range(0, len(self.cavern)):
                    line = ""
                    for x in range(0, len(self.cavern[y])):
                        p = Point(x, y)
                        unit = self.unit_at(p)
                        if unit is None:
                            line += self.cavern_tile_at(p)
                        else:
                            line += str(unit)
                    f.write(line + "\n")

    def show_hitpoints(self, filename=None):

        if filename is None:
            print('  UNIT  |  LOCATION  |   HP   |  ALIVE?  ')
            print('--------+------------+--------+----------')
            for u in self.all_units:
                unit = str(u).center(8)
                location = '{x}, {y}'.format(x=u.loc.x, y=u.loc.y).center(12)
                hp = str(u.hp).center(8)
                alive = str(u.is_alive()).center(10)
                print('{unit}|{location}|{hp}|{alive}'.format(
                    unit=unit,
                    location=location,
                    hp=hp,
                    alive=alive
                ))
        else:
            with open(filename, "w") as f:
                f.write('  UNIT  |  LOCATION  |   HP   |  ALIVE?  \n')
                f.write('--------+------------+--------+----------\n')
                for u in self.all_units:
                    unit = str(u).center(8)
                    location = '{x}, {y}'.format(
                        x=u.loc.x, y=u.loc.y).center(12)
                    hp = str(u.hp).center(8)
                    alive = str(u.is_alive()).center(10)
                    f.write('{unit}|{location}|{hp}|{alive}\n'.format(
                        unit=unit,
                        location=location,
                        hp=hp,
                        alive=alive
                    ))

    def play(self):
        turn_count = 0
        while len(self.alive_elves()) > 0 and len(self.alive_goblins()) > 0:
            turn_count += 1
            logging.info("Starting turn {turn_num}. {elf_count} Elves and {goblin_count} Goblins remaining.".format(
                turn_num=turn_count,
                elf_count=len(self.alive_elves()),
                goblin_count=len(self.alive_goblins())
            ))
            self.step(turn_count)
            # self.draw()
            # self.show_hitpoints()
            # print("")
            # self.draw("my_map/turn_{i}".format(i=turn_count))
            # self.show_hitpoints("my_hps/turn_{i}".format(i=turn_count))

        turn_count = turn_count - 1

        # Work out the winning team
        winning_team = Elf if len(self.alive_elves()) > 0 else Goblin

        # Get the total hit points remaining of the winning team
        remaining_hit_points = sum(
            [u.hp for u in self.all_units if type(u) == winning_team and u.is_alive()])

        return (turn_count, remaining_hit_points, winning_team)

    # Step through one round of combat
    def step(self, turn_num):
        # Fist get the order of the turn
        alive_units = filter(lambda u: u.is_alive(), self.all_units)
        unit_turn_order = self.order_units_by_position(alive_units)

        # Loop through each unit
        for unit in unit_turn_order:
            if not unit.is_alive():
                logging.debug("{unit} was killed in this round, so not taking its turn".format(
                    unit=unit.debug_str()
                ))
                continue

            logging.debug('Taking turn of {unit}'.format(
                unit=unit.debug_str()
            ))

            # Work out the list of all enemy units
            enemies = self.units(Goblin if type(unit) is Elf else Elf)

            alive_enemies = filter(lambda u: u.is_alive(), enemies)
            if len(alive_enemies) == 0:
                logging.info("All targets are dead!")
                return

            # Try and shortcut the routefinding, by seeing if there are targets
            # adjacent to us
            adjacent_targets = self.units_adjacent_to(
                type(enemies[0]), unit.loc)
            nearest_target = None
            if len(adjacent_targets) > 0:
                logging.debug("{u} is already adjacent to some targets ({targets})".format(
                    u=unit.debug_str(),
                    targets=map(lambda t: t.debug_str(), adjacent_targets)
                ))
                adjacent_targets = self.order_units_by_hit_points(
                    adjacent_targets)
                nearest_target = PathStep(0, adjacent_targets[0].loc)
            else:
                # Try an route to each enemy
                next_steps_to_targets = []

                # We have to try and route to all the targets, and find the nearest one
                for target in alive_enemies:

                    next_step = self.path_length(unit.loc, target.loc)
                    if not next_step is None:
                        logging.debug('Found a valid route between {unit} and {target}'.format(
                            unit=unit.debug_str(),
                            target=target.debug_str()
                        ))
                        next_steps_to_targets.append(next_step)

                # Check if there are any routeable targets
                if len(next_steps_to_targets) == 0:
                    continue

                # Sort the list of next steps by distance
                sorted_next_steps = sorted(
                    next_steps_to_targets, key=lambda ns: ns.d)
                min_dist = sorted_next_steps[0].d
                shortest_next_steps = filter(
                    lambda ns: ns.d == min_dist, sorted_next_steps)

                # Of the shortest next steps, sort them in reading order
                ordered_next_steps = sorted(
                    shortest_next_steps, key=lambda ns: ns.loc)
                next_step = ordered_next_steps[0]

                logging.debug('The first step for {unit} to make is {ns}'.format(
                    unit=unit.debug_str(),
                    ns=next_step
                ))

                # If the next step does not put you on top of the target (i.e. the distance >= 1), then move towards it
                if next_step.d > 0:
                    logging.debug(
                        "No targets in range. Moving towards nearest target")
                    unit.move_to(next_step.loc)

                    # Recalculate the nearest target
                    adjacent_targets = self.units_adjacent_to(
                        type(enemies[0]), unit.loc)
                    # Update where the nearest target is, if we are now in range of one
                    if len(adjacent_targets) > 0:
                        logging.debug("Moved in range of a target.")
                        adjacent_targets = self.order_units_by_hit_points(
                            adjacent_targets)
                        nearest_target = PathStep(0, adjacent_targets[0].loc)

            # Check if we are now in range of a target (either we just moved here
            # or we started in range of one)
            if not nearest_target is None and nearest_target.d == 0:
                logging.debug("Nearest target is in range. Attacking.")
                target_instance = self.unit_at(nearest_target.loc)
                unit.attack_target(target_instance)

        return

    # Find and return a list of all units of the given type that are adjacent to
    # the provided location
    def units_adjacent_to(self, unit_type, loc):
        adjacent_units = []
        u1 = self.unit_at(Point(loc.x, loc.y + 1))
        u2 = self.unit_at(Point(loc.x, loc.y - 1))
        u3 = self.unit_at(Point(loc.x + 1, loc.y))
        u4 = self.unit_at(Point(loc.x - 1, loc.y))
        for u in [u1, u2, u3, u4]:
            if u is None:
                continue
            if type(u) == unit_type and u.is_alive():
                adjacent_units.append(u)

        return adjacent_units

    # Check if there is a path between from and to avoiding other units and
    # walls. The path is valid even if there is a unit at from or to, but not if
    # there is a wall at either of those squares. If the path exists, return the
    # PathStep which corresponds to the first step to take, or None if no route
    # exists
    def path_length(self, from_point, to_point):
        logging.debug('Trying to find a path from {from_point} to {to_point}'.format(
            from_point=from_point,
            to_point=to_point
        ))

        if self.cavern_tile_at(from_point) == '#':
            return None
        if self.cavern_tile_at(to_point) == '#':
            return None

        q = [PathStep(0, to_point)]
        q_i = 0

        while q_i < len(q):
            ps = q[q_i]
            q_i += 1

            adj_cells = ps.loc.adjacent_points()
            adj_ps = map(lambda l: PathStep(ps.d + 1, l), adj_cells)

            # Check if the destination is in the adjacent points
            if from_point in map(lambda ps: ps.loc, adj_ps):
                q.append(PathStep(ps.d + 1, from_point))
                logging.debug("Added the destination coordinate.")
                break

            # Filter out all walls
            possible_ps = filter(
                lambda ps: self.cavern_tile_at(ps.loc) != '#', adj_ps)
            # Filter out other units
            possible_ps = filter(lambda ps: self.unit_at(
                ps.loc) is None, possible_ps)
            # Filter out all points with a shorter path step
            for poss_ps in possible_ps:
                cells_with_same_loc = filter(
                    lambda ps: ps.loc == poss_ps.loc, q)
                cells_with_shorter_distance = filter(
                    lambda ps: ps.d <= poss_ps.d, cells_with_same_loc)
                if len(cells_with_shorter_distance) == 0:
                    logging.debug("Adding {ps} to the queue.".format(
                        ps=poss_ps
                    ))
                    q.append(poss_ps)

        # Get all the routes that start at the right place (there should only
        # be one)
        possible_starts = filter(lambda ps: ps.loc == from_point, q)
        if len(possible_starts) == 0:
            logging.debug("No route available between {start} and {end}".format(
                start=from_point,
                end=to_point
            ))
            return None
        start = possible_starts[0]

        # Find all the steps adjacent to the starting location
        adj_steps = filter(lambda ps: start.loc.is_adjacent_to(ps.loc), q)

        # Find all the first steps that lead to the destination
        next_steps = filter(lambda ps: ps.d == start.d - 1, adj_steps)
        logging.debug('All possible next steps: {next_steps}'.format(
            next_steps=next_steps
        ))

        # Finally order the locations in reading order
        ordered_next_steps = sorted(next_steps, key=lambda ns: ns.loc)
        logging.debug("Choosing {ns} as the next step as it is first in reading order".format(
            ns=ordered_next_steps[0]
        ))
        return ordered_next_steps[0]


class Point(object):

    def __init__(self, x, y):
        super(Point, self).__init__()

        self.x = x
        self.y = y

    def adjacent_points(self):
        u1 = Point(self.x, self.y + 1)
        u2 = Point(self.x, self.y - 1)
        u3 = Point(self.x + 1, self.y)
        u4 = Point(self.x - 1, self.y)
        return [u1, u2, u3, u4]

    def is_adjacent_to(self, other):
        return self in other.adjacent_points()

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __gt__(self, other):
        if self.y > other.y:
            return True
        elif self.y < other.y:
            return False
        else:
            return self.x > other.x

    def __str__(self):
        return "({x}, {y})".format(
            x=self.x,
            y=self.y
        )


class PathStep(object):

    def __init__(self, distance, location):
        super(PathStep, self).__init__()

        self.d = distance
        self.loc = location

    def __eq__(self, other):
        logging.debug("{self_d} vs {other_d} and {self_loc} vs {other_loc}".format(
            self_d=self.d,
            other_d=other.d,
            self_loc=self.loc,
            other_loc=other.loc
        ))
        return self.d == other.d and self.loc == other.loc

    def __lt__(self, other):
        return self.d < other.d

    def __str__(self):
        return "({d}, {loc})".format(
            d=self.d,
            loc=self.loc
        )


class Unit(object):

    def __init__(self, location, hit_points=200, attack=3):
        super(Unit, self).__init__()

        self.loc = location

        self.hp = hit_points
        self._attack = attack

        self._is_alive = True

    def move_to(self, new_coordinate):
        logging.debug("Unit at {start} is moving to {end}".format(
            start=self.loc,
            end=new_coordinate
        ))
        self.loc = new_coordinate

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        logging.debug("Unit is now {u}".format(
            u=self.debug_str()
        ))

    def attack(self):
        return self._attack

    def attack_target(self, target):
        target.take_damage(self.attack())

    def debug_str(self):
        return "{type} {loc} : {hp}".format(
            type=str(self),
            loc=self.loc,
            hp=self.hp
        )


class Goblin(Unit):

    def __init__(self, location, hit_points=200, attack=3):
        super(Goblin, self).__init__(location, hit_points, attack)
        self.targets = [Elf]

    def __str__(self):
        return 'G'


class Elf(Unit):

    def __init__(self, location, hit_points=200, attack=3):
        super(Elf, self).__init__(location, hit_points, attack)
        self.targets = [Goblin]

    def __str__(self):
        return 'E'


if __name__ == '__main__':
    main()
