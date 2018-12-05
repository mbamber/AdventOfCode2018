#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Open and read the file
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    curr_totals = (0, 0)
    for word in file_contents:
        totals = two_and_three_count(word)
        curr_totals = tuple(map(sum, zip(curr_totals, totals)))

    checksum = curr_totals[0] * curr_totals[1]
    print('The checksum is {checksum}'.format(checksum=checksum))


# Work out the number of times 2 letters and 3 letters appear in a word
# Return two values of either 1 or 0 depending on if there are 2 letters or 3
def two_and_three_count(word):
    counts = letter_count(word)

    has_two_letters = len(filter(lambda k: counts[k] == 2, counts)) > 0
    has_three_letters = len(filter(lambda k: counts[k] == 3, counts)) > 0

    return (1 if has_two_letters else 0, 1 if has_three_letters else 0)

# Create a map of each letter to the number of times that it occurs
def letter_count(word):
    counts = {}

    for letter in word:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return counts

if __name__ == '__main__':
    main()
