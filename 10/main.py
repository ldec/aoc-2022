from queue import Queue
from typing import List

from utils.out import print
from utils.readers import OneColumnFileReader

NOOP = object()


class OperationReader(OneColumnFileReader):
    """
    Implementation of an operation reader

    E.g.

    noop
    addx 3
    addx -5
    """

    def read(self, *args):
        data = super(OperationReader, self).read()
        result = Queue()
        for row in data:
            if row == "noop":
                result.put(NOOP)
            else:
                result.put(int(row.split(" ")[1]))

        return result


def execute(data: Queue):
    x_history = []
    x = 1
    while not data.empty():
        operation = data.get()
        if operation == NOOP:
            x_history.append(x)
            continue

        x_history.append(x)
        x_history.append(x)
        x += operation

    x_history.append(x)

    cycles = [20, 60, 100, 140, 180, 220]
    signal_strength = []
    for index in cycles:
        signal_strength.append(x_history[index - 1] * index)

    return x_history, signal_strength


def draw(x_history: List[int]):
    result_raw = []
    result = []
    index = 0
    for y in range(0, 6):
        row = []
        for x in range(0, 40):
            signal = x_history[index]
            index += 1
            if signal - 1 == x or signal == x or signal + 1 == x:
                row.append("##")
            else:
                row.append("  ")
        result_raw.append(row)
        result.append("".join(row))

    print("\n".join(result))


def main():
    mini_test_reader = OperationReader("input-mini-test.txt")
    mini_test_data = mini_test_reader.read()

    test_reader = OperationReader("input-test.txt")
    test_data = test_reader.read()

    reader = OperationReader("input.txt")
    prod_data = reader.read()

    data_sources = (
        # ("Mini test data", mini_test_data),
        ("Test data", test_data),
        ("Prod data", prod_data),
    )

    for data_source_name, data_source in data_sources:
        x_history, signal_strength = execute(data_source)
        print(f"Day 1 - Result 1 - {data_source_name}: {sum(signal_strength)}")
        draw(x_history)


if __name__ == "__main__":
    main()
