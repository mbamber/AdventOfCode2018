#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    the_map = Map(map(lambda x: x.rstrip(), file_contents))
    the_map.draw()
    while len(the_map._carts) > 1:
        the_map.move_carts()


    print('There is only one cart left at: {loc}'.format(
        loc='({x}, {y})'.format(
            x=the_map._carts[0].x(),
            y=the_map._carts[0].y()
        )
    ))



class Cart():

    def __init__(self, x, y, dir):
        self._x = x
        self._y = y
        self.face(dir)
        self._next_junction_dir = 'l'
        self._is_collided = False

    def turn(self):
        # Work out what direction the cart is now facing, and what direction it
        # should turn next
        if self._next_junction_dir == 'l':
            if self._facing == '^':
                self.face('<')
            elif self._facing == '>':
                self.face('^')
            elif self._facing == 'v':
                self.face('>')
            elif self._facing == '<':
                self.face('v')
            else:
                raise ValueError('Cannot process turn for cart {cart} as could not identify current facing direction'.format(
                    cart=self
                ))

            self._next_junction_dir = 's'
        elif self._next_junction_dir == 's':
            # No need to change the direction we are facing, as we turned straight

            self._next_junction_dir = 'r'
        elif self._next_junction_dir == 'r':
            if self._facing == '^':
                self.face('>')
            elif self._facing == '>':
                self.face('v')
            elif self._facing == 'v':
                self.face('<')
            elif self._facing == '<':
                self.face('^')
            else:
                raise ValueError('Cannot process turn for cart {cart} as could not identify current facing direction'.format(
                    cart=self
                ))

            self._next_junction_dir = 'l'
        else:
            raise ValueError('Cannot process turn for cart {cart} as could not identify the next junction direction'.format(
                cart=self
            ))

    def x(self):
        return self._x

    def y(self):
        return self._y

    def facing(self):
        if self.is_collided():
            return 'X'
        else:
            return self._facing

    def mark_collided(self):
        self._is_collided = True

    def is_collided(self):
        return self._is_collided

    def face(self, dir):
        if dir not in ['^', '>', 'v', '<']:
            raise ValueError('{dir} is not a valid direction for the cart to face!'.format(
                dir=dir
            ))

        self._facing = dir

    # Move the cart based on its current facing
    def move(self):
        if self._facing == '^':
            self._y -= 1
        elif self._facing == '>':
            self._x += 1
        elif self._facing == 'v':
            self._y += 1
        elif self._facing == '<':
            self._x -= 1

class Map():

    def __init__(self, raw_data):
        self._carts = []
        self._map = self._generate_map(raw_data)

    def _generate_map(self, raw_data):
        map = []
        for y in range(0, len(raw_data)):
            map_row = []
            for x in range(0, len(raw_data[y])):
                cell = raw_data[y][x]
                map_row.append(self._process_cell(cell, x, y))
            map.append(map_row)

        return map

    # Get the map cell value given the raw input value, and add any carts to the
    # list of carts for this map
    def _process_cell(self, raw_cell, x, y):
        if raw_cell == '<' or raw_cell == '>':
            self._carts.append(Cart(x, y, raw_cell))
            return '-'

        if raw_cell == 'v' or raw_cell == '^':
            self._carts.append(Cart(x, y, raw_cell))
            return '|'

        return raw_cell

    # Order the list of carts, so the carts nearer the top left are at the front,
    # and carts near the bottom right are near the back
    def _order_carts(self):
        self._carts.sort(key=lambda cart: len(self._map[0]) * cart.y() + cart.x())

    def cell_at(self, x, y):
        return self._map[y][x]

    # Move all the carts
    def move_carts(self):
        self._order_carts()
        for cart in self._carts:
            cart.move()
            self.turn_cart(cart)
            self.mark_collisions()
        self.remove_colisions()

    def remove_colisions(self):
        if not self.is_collisions():
            return

        new_carts = filter(lambda c: not c.is_collided(), self._carts)
        self._carts = new_carts


    def turn_cart(self, cart):
        cart_cell = self.cell_at(cart.x(), cart.y())
        cart_facing = cart.facing()
        if cart_cell == '\\':
            if cart_facing == '^':
                cart.face('<')
            elif cart_facing == '>':
                cart.face('v')
            elif cart_facing == 'v':
                cart.face('>')
            elif cart_facing == '<':
                cart.face('^')
            else:
                raise RuntimeError('Something went wrong trying to turn the cart at a corner')
        elif cart_cell == '/':
            if cart_facing == '^':
                cart.face('>')
            elif cart_facing == '>':
                cart.face('^')
            elif cart_facing == 'v':
                cart.face('<')
            elif cart_facing == '<':
                cart.face('v')
            else:
                raise RuntimeError('Something went wrong trying to turn the cart at a corner')
        elif cart_cell == '+':
            cart.turn()

    def cart_at(self, x, y):
        carts_at_coords = filter(lambda cart: cart.x() == x and cart.y() == y, self._carts)
        if len(carts_at_coords) > 0:
            return carts_at_coords[0]
        else:
            return None

    def mark_collisions(self):
        for cart1_index in range(0, len(self._carts) - 1):
            cart1 = self._carts[cart1_index]
            if cart1.is_collided():
                continue
            for cart2_index in range(cart1_index + 1, len(self._carts)):
                cart2 = self._carts[cart2_index]
                if cart2.is_collided():
                    continue
                if cart1.x() == cart2.x() and cart1.y() == cart2.y():
                    cart1.mark_collided()
                    cart2.mark_collided()

    def is_collisions(self):
        collided_carts = filter(lambda cart: cart.is_collided(), self._carts)
        return len(collided_carts) > 0

    def get_collisions(self):
        collided_carts = filter(lambda cart: cart.is_collided(), self._carts)
        return collided_carts

    def draw(self):
        for y in range(0, len(self._map)):
            for x in range(0, len(self._map[y])):
                cart_at_coord = self.cart_at(x, y)
                if cart_at_coord == None:
                    print(self.cell_at(x, y), end='')
                else:
                    print(cart_at_coord.facing(), end='')

            print('')

if __name__ == '__main__':
    main()
