#! /usr/bin
# -*- coding: UTF-8 -*-

from __future__ import print_function

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    input = str(file_contents[0].rstrip())

    elf_1_index = 0
    elf_2_index = 1

    # The starting recipes
    recipe_list = [3, 7]

    tail = []
    while not input in ''.join(map(str, tail)):
        tail = recipe_list[-1 * (2 + len(input)):]
        recipe_list += generate_new_recipes(elf_1_index, elf_2_index, recipe_list)
        elf_1_index = get_next_recipe_index(elf_1_index, recipe_list)
        elf_2_index = get_next_recipe_index(elf_2_index, recipe_list)

    print('{input} first appears after {start} recipes.'.format(
        input=input,
        start=''.join(map(str, recipe_list)).index(input)
    ))


def print_recipe_list(i1, i2, recipe_list):
    for i in range(0, len(recipe_list)):
        if i == i1:
            print('({val})'.format(val=recipe_list[i]), end='')
        elif i == i2:
            print('[{val}]'.format(val=recipe_list[i]), end='')
        else:
            print(' {val} '.format(val=recipe_list[i]), end='')
    print('')

def generate_new_recipes(index1, index2, recipe_list):
    r1 = recipe_list[index1]
    r2 = recipe_list[index2]
    new_recipe_scores = r1 + r2
    return map(int, list(str(new_recipe_scores)))


def get_next_recipe_index(starting_index, recipe_list):
    next_recipe_index = starting_index + 1 + recipe_list[starting_index]
    next_recipe_index = next_recipe_index % len(recipe_list)
    return next_recipe_index

if __name__ == '__main__':
    main()
