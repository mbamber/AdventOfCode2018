#! /usr/bin
# -*- coding: UTF-8 -*-

import sys

def main():

    # Open the file
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()


    # Keep a track of the used totals
    used_totals = [0]

    # Loop through each line, and sum the files
    curr_total = 0
    while True:
        for line in file_contents:
            try:
                int_val = int(line)
                curr_total += int_val
                if curr_total in used_totals:
                    print('The first total that is repeated is {repeated_total}'.format(repeated_total=curr_total))
                    sys.exit(0)
                used_totals.append(curr_total)
            except ValueError as ve:
                raise ve

if __name__ == '__main__':
    main()
