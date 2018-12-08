#! /usr/bin
# -*- coding: UTF-8 -*-

def main():

    # Load in the polymer
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    polymer = file_contents[0].rstrip()

    curr_shortest_polymer = (None, 9999999999)
    for char in "abcdefghijklmnopqrstuvwxyz":
        curr_polymer = polymer
        curr_polymer = curr_polymer.replace(char, '')
        curr_polymer = curr_polymer.replace(char.upper(), '')
        reacted_polymer = react_polymer(curr_polymer)

        print('Length of polymer without {removed_unit} is {length}'.format(
            removed_unit=char,
            length=len(reacted_polymer)
        ))

        if len(reacted_polymer) < curr_shortest_polymer[1]:
            curr_shortest_polymer = (reacted_polymer, len(reacted_polymer))

    print('The shortest polymer is {new_polymer} which has {num_units} units'.format(
        new_polymer=curr_shortest_polymer[0],
        num_units=curr_shortest_polymer[1]
    ))

def react_polymer(polymer):

    # Keep looping through the polymer until we didnt make a change
    did_make_change_in_pass = True
    while did_make_change_in_pass:

        did_make_change_in_pass = False
        new_polymer = ''

        # Loop through the polymer, performing all the reactions
        i = 0
        while i < (len(polymer) - 1):
            reaction_result = attempt_reaction(polymer[i], polymer[i+1])
            new_polymer = new_polymer + reaction_result

            if reaction_result == '':
                did_make_change_in_pass = True
                i += 1 # We need to skip the next unit, because it just reacted and dissapeared

            i += 1

        # Need to add the last unit in the polymer if it didnt react with the
        # second-last unit, or the last attempted reaction succeded, but it was
        # on the third last and second last units (i.e. the last unit is untouched)
        if (not reaction_result == '') or (reaction_result == '' and (i < len(polymer))):
            new_polymer = new_polymer + polymer[len(polymer) - 1]

        polymer = new_polymer

    return polymer

# See if two units react, and either return an empty string (because they anihilated themselves)
# or the first unit because there was no reaction
def attempt_reaction(x, y):

    # Check if the cases match
    if x.isupper() and y.isupper():
        return x

    if x.islower() and y.islower():
        return x

    # Given that the cases do not match, check if they are the same letter
    if x.upper() == y.upper():
        return ''
    else:
        return x


if __name__ == '__main__':
    main()
