from os.path import isfile
from typing import List, Any, Optional


class Reader:
    """
    Base class for Reader implementation.
    """

    def read(self, *args, **kwargs):
        """
        Base implem of the read function
        """
        raise NotImplementedError


class FileReader(Reader):
    """
    Base class for file Reader implementation

    Support basic file reading
    """

    file = None

    def __init__(self, file: str) -> None:
        assert isfile(file), f"Cannot import file {file}"
        self.file = file

    def read(self, *args, **kwargs) -> str:
        """
        Base implementation of a file read function
        """
        with open(self.file, "r") as f:
            return f.read()


class OneColumnFileReader(FileReader):
    """
    Implementation of a one column data file Reader

    E.g.

    1
    2
    3
    """

    def read(
        self, *args, type_to_cast: Any = None, sort: bool = False, **kwargs
    ) -> List:
        """
        Implementation of a one column data file read function

        :param type_to_cast: Optional type casting for each line
        :param sort: Sort the list
        """
        data = super(OneColumnFileReader, self).read()
        split_data = [line for line in data.splitlines() if line]
        if type_to_cast is not None:
            split_data = list(map(type_to_cast, split_data))
        if sort:
            split_data = sorted(split_data)
        return split_data


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

    def read(
        self, *args, type_to_cast: Any = None, sort: bool = False, **kwargs
    ) -> List[List]:
        """
        Implementation of a one column space aware data file read function

        :param type_to_cast: Optional type casting for each line
        :param sort: Sort the list
        """
        data = super(OneColumnFileReaderSpaceAware, self).read()
        split_data = data.splitlines()

        indexes = [i for i, x in enumerate(split_data) if not x]

        result = []
        for start, end in zip([0, *indexes], [*indexes, len(split_data)]):
            chunk = [line for line in split_data[start : end + 1] if line]
            if type_to_cast is not None:
                chunk = list(map(type_to_cast, chunk))
            if sort:
                chunk = sorted(chunk)
            result.append(chunk)

        return result
