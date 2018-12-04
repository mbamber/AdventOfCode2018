#! /usr/bin
# -*- coding: UTF-8 -*-

import sys

def main():

    # Open and read the file
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    for i in range(0, len(file_contents)):
        first_word = file_contents[i]
        for j in range(i+1, len(file_contents)):
            second_word = file_contents[j]

            for x in range(1, 5):
                if get_word_without_char(first_word, x) == get_word_without_char(second_word, x):
                    print('The two words are {first_word} and {second_word}'.format(
                        first_word=first_word,
                        second_word=second_word
                    ))
                    print('The common part is {common_word} and the differing position is {pos}'.format(
                        common_word=get_word_without_char(first_word, x),
                        pos=x
                    ))
                    sys.exit(0)

# Remove the given character position from the specified word
def get_word_without_char(word, char_pos):
    first_part = word[:char_pos-1]
    second_part = word[char_pos:]
    return first_part + second_part

if __name__ == '__main__':
    main()
