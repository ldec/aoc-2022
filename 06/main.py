import more_itertools
from utils.out import print
from utils.readers import FileReader

test_reader = FileReader("input-test.txt")
test_data = test_reader.read()

reader = FileReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def find_packet(data: str, window_size: int) -> int:
    """
    Given a string, return the index of the first character found after the first
    windows composed of unique characters.
    """
    windows = more_itertools.sliding_window(data, window_size)
    for index, window in enumerate(windows):
        char_set = set(window)
        if len(char_set) == len(window):
            return index + window_size


for data_source_name, data_source in data_sources:
    print(f"Day 1 - Result 1 - {data_source_name}: {find_packet(data_source, 4)}")
    print(f"Day 1 - Result 1 - {data_source_name}: {find_packet(data_source, 14)}")
