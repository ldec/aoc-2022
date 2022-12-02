from typing import List

from rich import print

from utils.readers import FileReader


class OneColumnFileReaderSpaceAware(FileReader):
    """
    Implementation of a one column data file Reader with space awerness

    E.g.

    1
    2
    3

    5
    6
    7

    ->
    [[1, 2, 3], [[5, 6 ,7]]
    """

    def read(self, *args) -> List[List]:
        """
        Implementation of a one column space aware data file read function
        """
        data = super(OneColumnFileReaderSpaceAware, self).read()
        split_data = data.splitlines()

        indexes = [i for i, x in enumerate(split_data) if not x]

        result = []
        for start, end in zip([0, *indexes], [*indexes, len(split_data)]):
            chunk = [line for line in split_data[start : end + 1] if line]
            chunk = list(map(int, chunk))
            result.append(chunk)

        return result


test_reader = OneColumnFileReaderSpaceAware("input-test.txt")
test_data = test_reader.read()

reader = OneColumnFileReaderSpaceAware("input.txt")
prod_data = reader.read()

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
