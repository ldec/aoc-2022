from typing import List, Set

from utils.out import print
from utils.readers import OneColumnFileReader


def range_to_set(data: str):
    """
    Convert a vlan like range to an int set

    2-4 -> set(2, 3, 4)
    """
    min, max = map(int, data.split("-"))
    return set(range(min, max + 1))


class AssignmentReader(OneColumnFileReader):
    """
    Implementation of an assignment pair

    E.g.

    2-4,6-8
    2-3,4-5

    ->
    [[(2, 3, 4), (6, 7, 8)], [(2, 3), (4, 5)]]
    """

    def read(self, *args) -> List[List[Set[int]]]:
        """
        Implementation of a one column assignment pair file read function
        """
        data = super(AssignmentReader, self).read()
        result = []
        for line in data:
            left, right = line.split(",")
            assignment = [range_to_set(left), range_to_set(right)]
            result.append(assignment)

        return result


test_reader = AssignmentReader("input-test.txt")
test_data = test_reader.read()

reader = AssignmentReader("input.txt")
prod_data = reader.read()

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def check_for_fully_contains_set(left: Set[int], right: Set[int]):
    """
    Given two sets, check if any of them is a subset of the other
    """
    return left.issubset(right) or right.issubset(left)


def check_for_fully_contains_sets(data: List[List[Set[int]]]) -> int:
    """
    Given a list of pair assignment, check the number of pair where an assignment is
    the subset of the other
    """
    result = 0
    for pair in data:
        if check_for_fully_contains_set(*pair):
            result += 1

    return result


def check_for_intersection_set(left: Set[int], right: Set[int]):
    """
    Given two sets, check is they are intersecting
    """
    return left.intersection(right)


def check_for_intersection_sets(data: List[List[Set[int]]]) -> int:
    """
    Given a list of pair assignment, check the number of pair assignments are intersecting
    """
    result = 0
    for pair in data:
        if check_for_intersection_set(*pair):
            result += 1

    return result


for data_source_name, data_source in data_sources:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {check_for_fully_contains_sets(data_source)}"
    )
    print(
        f"Day 1 - Result 2 - {data_source_name}: {check_for_intersection_sets(data_source)}"
    )
