#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Read the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    # Initialize the fabric
    fabric = []
    for y in range(0, 1000):
        fabric_row = []
        for x in range(0, 1000):
            fabric_row.append(0)
        fabric.append(fabric_row)

    # Plot each rectangle
    for rect in file_contents:
        fabric = plot_rect(fabric, rect.rstrip())

    # print_fabric(fabric)

    overlapping = count_overlapping(fabric)
    print('There are {total} square inches overlapping between claims'.format(
        total=overlapping
    ))

def plot_rect(fabric, rect):
    rect_details = get_rect_details(rect)

    for y in range(rect_details['y'], rect_details['y'] + rect_details['height']):
        for x in range(rect_details['x'], rect_details['x'] + rect_details['width']):
            fabric[y][x] += 1

    return fabric


def get_rect_details(rect):
    parts1 = rect.split(' @ ')
    id = parts1[0]

    parts2 = parts1[1].split(': ')
    x, y = map(int, parts2[0].split(','))
    w, h = map(int, parts2[1].split('x'))

    return {'id':id, 'x':x, 'y':y, 'width':w, 'height':h}

def count_overlapping(fabric):
    total = 0
    for row in fabric:
        for cell in row:
            if cell > 1:
                total += 1

    return total

def print_fabric(fabric):
    for row in fabric:
        print row

if __name__ == '__main__':
    main()
