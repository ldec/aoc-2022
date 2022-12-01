from typing import List

from utils.readers import OneColumnFileReaderSpaceAware
from rich import print

test_reader = OneColumnFileReaderSpaceAware("input-test.txt")
test_data = test_reader.read(type_to_cast=int)

reader = OneColumnFileReaderSpaceAware("input.txt")
prod_data = reader.read(type_to_cast=int)

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def combine_calories(data: List[List[int]]) -> List[int]:
    """
    Given a list of items by elf, return the list of combined values by elf
    """
    result = []
    for elf in data:
        calories = sum(elf)
        result.append(calories)
    return result


def top_three_combined(data: List[int]) -> int:
    """
    Given the list of calories by elf, return the combined calories of the top three
    calories carrying elves.
    """
    data = sorted(data, reverse=True)
    return sum(data[0:3])


for data_source_name, data_source in data_sources:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {max(combine_calories(data_source))}"
    )
    print(
        f"Day 1 - Result 2 - {data_source_name}: {top_three_combined(combine_calories(data_source))}"
    )
