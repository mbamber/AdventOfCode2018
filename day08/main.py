#! /usr/bin
# -*- coding: UTF-8 -*-

import uuid

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()[0].rstrip()

    data = file_contents.split(' ')
    data = map(lambda x: int(x), data)

    initial_header = data[:2]
    initial_data = data[2:]

    num_subtrees = initial_header[0]
    num_metadata = initial_header[1]

    root = Tree(num_subtrees, num_metadata)

    root, data = generate_subtrees(root, initial_data)

    print('The whole tree has sum of metadata {metadata_sum}'.format(
        metadata_sum=root.get_metadata_sum()
    ))

# Generate a tree recursively from the given set of data
def generate_subtrees(node, data):

    # Work down the tree, looking at all of the subtrees
    while node.num_subtrees() > len(node.subtrees()):
        next_child = Tree(data[0], data[1])
        new_data = data[2:]
        # Call recursively for each subtree
        t, data = generate_subtrees(next_child, new_data)
        node.add_subtree(t)

    # Once all the  subtrees have been generated, get the metadata for this node
    for i in range(0, node.num_metadata()):
        node.add_metadata(data[i])
    data = data[node.num_metadata():]
    return node, data

class Tree:

    def __init__(self, num_subtrees, num_metadata):
        self._num_subtrees = num_subtrees
        self._num_metadata = num_metadata
        self._subtrees = []
        self._metadata = []
        self._id = uuid.uuid4()

    def subtrees(self):
        return self._subtrees

    def add_subtree(self, t):
        self._subtrees.append(t)

    def num_subtrees(self):
        return self._num_subtrees

    def num_metadata(self):
        return self._num_metadata

    def add_metadata(self, m):
        self._metadata.append(m)

    def metadata(self):
        return self._metadata

    def get_metadata_sum(self):
        my_sum = sum(self._metadata)
        subtree_sum = 0
        for st in self.subtrees():
            subtree_sum += st.get_metadata_sum()

        return my_sum + subtree_sum

    def is_tree_complete(self):
        return len(self.subtrees()) == self.num_subtrees and len(self._metadata) == self.num_metadata

    def __str__(self):
        return '<metadata: {metadata}, subtrees: {subtrees}, num_metadata: {num_metadata}, num_subtrees: {num_subtrees}>'.format(
            metadata=self._metadata,
            subtrees=self._subtrees,
            num_metadata=self._num_metadata,
            num_subtrees=self._num_subtrees
        )

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    main()
