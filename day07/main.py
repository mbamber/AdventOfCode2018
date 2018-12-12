#! /usr/bin
# -*- coding: UTF-8 -*-

import re

LETTER_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    # Build a mapping of the direct decendants
    direct_decendants = {}
    for l in LETTER_LIST:
        direct_decendants[l] = []

    # Use a regex to find the dependencies
    regex = 'Step (.) must be finished before step (.) can begin.'
    compiled_regex = re.compile(regex)
    for instruction in file_contents:
        matches = re.findall(compiled_regex, instruction)[0]
        direct_decendants[matches[0]].append(matches[1])

    direct_decendants = reverse_map(direct_decendants)

    ordered_instructions = ''

    while len(direct_decendants) > 0:
        next_instruction, direct_decendants = get_next_instruction(direct_decendants)
        ordered_instructions += next_instruction

    print('The final order of instructions is: {final_order}'.format(
        final_order=ordered_instructions
    ))

def reverse_map(initial_map):
    new_map = {}
    for l in LETTER_LIST:
        new_map[l] = []

    for letter in initial_map:
        for dependent in initial_map[letter]:
            new_map[dependent].append(letter)

    return new_map

def get_next_instruction(direct_decendants):
    instructions_without_dependencies = get_instructions_without_dependencies(direct_decendants)
    sorted_instructions = sorted(instructions_without_dependencies)
    instruction = sorted_instructions[0]

    new_dependencies = remove_instruction_from_map(instruction, direct_decendants)

    return (instruction, new_dependencies)

def remove_instruction_from_map(instruction, direct_decendants):
    new_dependencies = {}
    for letter in direct_decendants:
        # Don't readd the one we want to remove
        if instruction == letter:
            continue

        # Remove the instruction from all of the dependency lists
        dependencies = direct_decendants[letter]
        new_dependency_list = []
        for d in dependencies:
            if not d == instruction:
                new_dependency_list.append(d)

        new_dependencies[letter] = new_dependency_list

    return new_dependencies

def get_instructions_without_dependencies(direct_decendants):
    instructions = filter(lambda instruction: len(direct_decendants[instruction]) == 0, direct_decendants)
    return instructions

if __name__ == '__main__':
    main()
