#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Open the file
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()


    # Loop through each line, and sum the files
    curr_total = 0
    for line in file_contents:
        try:
            int_val = int(line)
            curr_total += int_val
        except ValueError as ve:
            raise ve

    print('The total is {total}'.format(total=curr_total))

if __name__ == '__main__':
    main()
