from copy import copy
from typing import List

from rich import print

from utils.readers import OneColumnFileReader


class RucksackReader(OneColumnFileReader):
    """
    Implementation of a rucksack inventory

    E.g.

    aaaBBB
    cccDDD

    ->
    [[aaa, BBB], [ccc, DDD]]
    """

    def read(self, *args) -> List[List]:
        """
        Implementation of a one column space aware data file read function
        """
        data = super(RucksackReader, self).read()
        result = []
        for line in data:
            split = int(len(line) / 2)
            rucksack = [line[:split], line[split:]]
            result.append(rucksack)

        return result


test_reader = RucksackReader("input-test.txt")
test_data = test_reader.read()

reader = RucksackReader("input.txt")
prod_data = reader.read()

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def find_common_letter_in_rucksack(left: str, right: str) -> str:
    """
    Given two strings, return the common letter.
    """
    for letter in left:
        if letter in right:
            return letter

    raise Exception(f"Could not find common letter in {left} & {right}")


def compute_prio(letter: str) -> int:
    """
    Given an item, compute the associated priority
    """
    if letter.islower():
        return ord(letter) - 96
    return ord(letter) - 64 + 26


def compute_all_prio(rucksacks: List[List[str]]) -> int:
    """
    Given a list of rucksacks, compute the sum of all rucksack priority
    """
    result = 0
    for rucksack in rucksacks:
        common_letter = find_common_letter_in_rucksack(*rucksack)
        prio = compute_prio(common_letter)
        result += prio
        print(
            f"rucksack : {rucksack}, CL: {common_letter}, prio: {prio}, res: {result}"
        )

    return result


def chunks(lst, n):
    """
    Given a list, return the list divided in chunks of n length
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def find_common_letter_in_multiple_rucksack(rucksacks: List[List[str]]) -> str:
    """
    Given a list of rucksacks, find the common item
    """
    rucksacks_merged = [rucksack[0] + rucksack[1] for rucksack in rucksacks]
    for rucksack in rucksacks_merged:
        rucksacks_to_compare = copy(rucksacks_merged)
        rucksacks_to_compare.remove(rucksack)
        for letter in rucksack:
            found = len(
                list(filter(lambda x: letter in x, rucksacks_to_compare))
            ) == len(rucksacks_to_compare)
            if found:
                return letter

    raise Exception()


def compute_badge_prio(rucksacks: List[List[str]]) -> int:
    """
    Given a list of rucksacks, device them in groups of three, find the common items in
    all rucksack groups and sum them.
    """
    groups = chunks(rucksacks, 3)
    result = 0
    for group in groups:
        common_letter = find_common_letter_in_multiple_rucksack(group)
        prio = compute_prio(common_letter)
        result += prio
        print(f"rucksack : {group}, CL: {common_letter}, prio: {prio}, res: {result}")

    return result


for data_source_name, data_source in data_sources:
    print(f"Day 1 - Result 1 - {data_source_name}: {compute_all_prio(data_source)}")
    print(f"Day 1 - Result 2 - {data_source_name}: {compute_badge_prio(data_source)}")
