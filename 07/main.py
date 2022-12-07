from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from rich.tree import Tree

from utils.out import print
from utils.readers import FileReader


class Directory:
    pass


@dataclass
class File:
    name: str
    size: int
    parent: Directory

    def to_tree(self, tree: Tree):
        tree.add(f"{self.name} - {self.size}")
        return tree


@dataclass
class Directory:
    name: str
    content: List
    parent: Optional[Directory]

    def to_tree(self, tree: Tree):
        subtree = tree.add(f"{self.name}")
        for content in self.content:
            subtree = content.to_tree(subtree)
        return tree

    @property
    def size(self) -> int:
        return sum(map(lambda x: x.size, self.content))

    def contains_file(self, file: File):
        for content in self.content:
            if type(content) == File and content.name == file.name:
                return content
        return None

    def contains_dir(self, dir: Directory):
        for content in self.content:
            if type(content) == Directory and content.name == dir.name:
                return content
        return None


def line_to_file_or_dir(line, parent: Directory):
    if "dir" in line:
        line = line.replace("dir ", "")
        return Directory(name=line, content=list(), parent=parent)
    size, name = line.split(" ")
    return File(name=name, size=int(size), parent=parent)


class CommandType(Enum):
    CD = 1
    LS = 2


def to_command_type(input: str) -> CommandType:
    if input.startswith(" cd"):
        return CommandType.CD
    if input.startswith(" ls"):
        return CommandType.LS


class CommandReader(FileReader):
    """
    Implementation of a command reader

    E.g.

    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    """

    def read(self, *args):
        """
        Implementation of a one column space aware data file read function
        """
        data = super(CommandReader, self).read()
        data = data.split("$")
        data = [line for line in data if line]

        root = Directory(name="/", content=list(), parent=None)
        current_directory = root

        for raw_command in data[1:]:
            command_type = to_command_type(raw_command)
            if command_type == CommandType.CD:
                dir_name = raw_command.split(" ")[2].strip()
                if dir_name == "..":
                    current_directory = current_directory.parent
                    continue

                target = current_directory.contains_dir(
                    Directory(name=dir_name, content=list(), parent=None)
                )
                assert target is not None
                current_directory = target

            if command_type == CommandType.LS:
                raw_command = raw_command.splitlines()
                result = raw_command[1:]
                for line in result:
                    item = line_to_file_or_dir(line, parent=current_directory)
                    if type(item) == File:
                        # Is the file already in the dir ?
                        if current_directory.contains_file(item) is None:
                            current_directory.content.append(item)
                    else:
                        # Is the dir already in the dir ?
                        if current_directory.contains_dir(item) is None:
                            current_directory.content.append(item)
        return root


test_reader = CommandReader("input-test.txt")
test_data = test_reader.read()

reader = CommandReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def find_small_directories(root: Directory) -> List[Directory]:
    """
    Given a root directory, find all the small directories
    """
    result = []
    for content in root.content:
        if type(content) == Directory:
            if content.size < 100000:
                result.append(content)
            result.extend(find_small_directories(content))

    return result


def find_smallest_directory_to_delete(root: List, min: int) -> Directory:
    """
    Given a root directory, find the smallest directory above the min size
    """
    smallest_directory_to_delete = root
    for content in root.content:
        if type(content) == Directory:
            if min < content.size < smallest_directory_to_delete.size:
                smallest_directory_to_delete = content

            smallest_directory_to_delete_child = find_smallest_directory_to_delete(
                content, min
            )
            if (
                smallest_directory_to_delete.size
                > smallest_directory_to_delete_child.size
                > min
            ):
                smallest_directory_to_delete = smallest_directory_to_delete_child

    return smallest_directory_to_delete


for data_source_name, data_source in data_sources:
    tree = Tree("File system")
    tree = data_source.to_tree(tree)
    print(f"Day 1 - Result 1 - {data_source_name}:")
    print(tree)

    small_directories = find_small_directories(data_source)
    small_directories_total_size = sum(map(lambda x: x.size, small_directories))
    print(f"Day 1 - Result 1 - {data_source_name}: {small_directories_total_size}")

    unused_space = 70000000 - data_source.size
    to_free = 30000000 - unused_space

    smallest_directory_to_delete = find_smallest_directory_to_delete(
        data_source, to_free
    )
    print(f"Day 1 - Result 2 - {data_source_name}: {smallest_directory_to_delete.size}")
