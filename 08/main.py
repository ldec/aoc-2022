from dataclasses import dataclass

import numpy as np
from rich.tree import Tree

from utils.math import multiply
from utils.out import print
from utils.readers import OneColumnFileReader


@dataclass
class Tree:
    x: int
    y: int
    height: int
    shape: tuple

    def on_edge(self):
        """
        Is the tree on  the edge ?
        """
        return (
            self.x == 0
            or self.y == 0
            or self.x == self.shape[0] - 1
            or self.y == self.shape[1] - 1
        )


class TreeMapReader(OneColumnFileReader):
    """
    Implementation of a tree map reader

    E.g.

    30373
    25512
    65332
    33549
    35390
    """

    def read(self, *args):
        data = super(TreeMapReader, self).read()
        raw_array = []
        for row in data:
            raw_array.append(list(map(int, list(row))))
        return np.array(raw_array)


test_reader = TreeMapReader("input-test.txt")
test_data = test_reader.read()

reader = TreeMapReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def is_tree_hidden(tree_map: np.ndarray, tree: Tree):
    """
    Given a tree map and a tree, check is the tree is hidden, and if it is, compute
    it's scenic score.
    """
    if tree.on_edge():
        return False, 0

    row = tree_map[tree.y]
    column = tree_map[:, tree.x]

    to_compare_list = [
        list(reversed(column[: tree.y])),  # up
        list(reversed(row[: tree.x])),  # left
        column[tree.y + 1 :],  # down
        row[tree.x + 1 :],  # right
    ]

    scenic_scores = []
    is_hidden = []
    for to_compare in to_compare_list:
        scenic_score = 0
        is_hidden_local = False
        for index, other_tree in enumerate(to_compare):
            if index == 0:
                scenic_score += 1
            else:
                if other_tree <= tree.height:
                    scenic_score += 1
                if other_tree == tree.height:
                    break

        for other_tree in to_compare:
            if other_tree >= tree.height:
                is_hidden_local = True

        scenic_scores.append(scenic_score)
        is_hidden.append(is_hidden_local)

    return all(is_hidden), multiply(scenic_scores)


def compute_visible_tree_number(tree_map: np.ndarray) -> int:
    """
    Given a tree map, compute the number of visible trees
    """
    visible_trees = 0
    for tree in np.ndenumerate(tree_map):
        hidden, score = is_tree_hidden(
            tree_map,
            Tree(x=tree[0][1], y=tree[0][0], height=tree[1], shape=tree_map.shape),
        )
        if not hidden:
            visible_trees += 1

    return visible_trees


def compute_best_scenic_score(tree_map: np.ndarray) -> int:
    """
    Given a tree map, compute the best scenic score possible
    """
    best_scenic_score = 0
    for tree in np.ndenumerate(tree_map):
        hidden, score = is_tree_hidden(
            tree_map,
            Tree(x=tree[0][1], y=tree[0][0], height=tree[1], shape=tree_map.shape),
        )
        if not hidden and score > best_scenic_score:
            best_scenic_score = score

    return best_scenic_score


for data_source_name, data_source in data_sources:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {compute_visible_tree_number(data_source)}"
    )
    print(
        f"Day 1 - Result 2 - {data_source_name}: {compute_best_scenic_score(data_source)}"
    )
