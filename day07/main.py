#! /usr/bin
# -*- coding: UTF-8 -*-

import re

LETTER_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_WORKERS = 5
TASK_DEFAULT_TIME = 60

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

    # Create a mapping of a finish time to tasks that are in progress
    in_progress_tasks = {}
    # Maintain a mapping of workers to the task they are currently working on
    available_workers = {}
    for i in range(0, NUM_WORKERS):
        available_workers[i + 1] = None

    t = 0
    is_done = False
    while not is_done:
        # Stop any tasks that have now finished
        new_finished_tasks = []
        if t in in_progress_tasks:
            new_finished_tasks = in_progress_tasks.pop(t)

        # Update the list of task letters that are in progress
        task_letters_in_progress = []
        for ipt_time in in_progress_tasks:
            task_letters_in_progress += in_progress_tasks[ipt_time]
        task_letters_in_progress = list(set(task_letters_in_progress))

        # Update the list of workers that are now free
        for worker in available_workers:
            curr_task = available_workers[worker]
            if curr_task in new_finished_tasks:
                available_workers[worker] = None

        # Update the dependency mapping to remove the tasks that are now complete
        for finished_task in new_finished_tasks:
            direct_decendants = remove_instruction_from_map(finished_task, direct_decendants)

        # Update the list of tasks that can be started
        tasks_ready_to_start = get_instructions_without_dependencies(direct_decendants)
        tasks_ready_to_start = filter(lambda x: x not in task_letters_in_progress, tasks_ready_to_start)

        # Start any new tasks
        for worker in available_workers:
            if available_workers[worker] == None:
                if len(tasks_ready_to_start) > 0:
                    task_to_start = tasks_ready_to_start.pop()
                    task_finish_time = task_completion_time(task_to_start) + t

                    # Assign the worker to the task
                    available_workers[worker] = task_to_start
                    # Add the task to the list of in_progress_tasks
                    if task_finish_time in in_progress_tasks:
                        in_progress_tasks[task_finish_time].append(task_to_start)
                    else:
                        in_progress_tasks[task_finish_time] = [task_to_start]

        # Decide if we have completed all the tasks
        if len(direct_decendants) == 0 and len(in_progress_tasks) == 0:
            is_done = True
            continue

        t += 1

    print('Tasks completed after {secs} seconds'.format(
        secs=t
    ))


def reverse_map(initial_map):
    new_map = {}
    for l in LETTER_LIST:
        new_map[l] = []

    for letter in initial_map:
        for dependent in initial_map[letter]:
            new_map[dependent].append(letter)

    return new_map

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

def task_completion_time(task):
    return ord(task) - 64 + TASK_DEFAULT_TIME

if __name__ == '__main__':
    main()
