import re
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Dict, Tuple

from utils.out import print
from utils.readers import FileReader

INSTRUCTION_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")


@dataclass
class Instruction:
    number: int
    origin: int
    destination: int


class CraneStackReader(FileReader):
    """
    Implementation of a crane stack pair

    E.g.

        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
    """

    def read_stack(self, raw_stack: List[str]) -> Dict[int, deque]:
        """
        Given a raw stack, return a modelized stack
        """
        index_line = raw_stack[-1]
        index_to_col_map = {}
        stacks = {}

        for index, char in enumerate(index_line):
            if char != " ":
                index_to_col_map[index] = int(char)
                stacks[int(char)] = deque()

        for line in raw_stack[:-1]:
            for char_index, char in enumerate(line):
                if char not in ["[", "]", " ", ""]:
                    stack_index = index_to_col_map.get(char_index)
                    assert stack_index is not None
                    stacks[stack_index].append(char)

        return stacks

    def read_instructions(self, raw_instructions: List[str]) -> List[Instruction]:
        """
        Given a list of raw instructions, return a list of instructions
        """
        instructions = []
        for line in raw_instructions:
            number, origin, destination = INSTRUCTION_REGEX.match(line).groups()
            instruction = Instruction(
                number=int(number), origin=int(origin), destination=int(destination)
            )
            instructions.append(instruction)

        return instructions

    def read(self, *args) -> Tuple[Dict[int, deque], List[Instruction]]:
        """
        Implementation of a combined crane stack and insturction file reader.
        """
        data = super(CraneStackReader, self).read().splitlines()

        empty_line = data.index("")
        raw_stack, raw_instructions = data[:empty_line], data[empty_line + 1 :]

        stack = self.read_stack(raw_stack)
        instructions = self.read_instructions(raw_instructions)

        return stack, instructions


test_reader = CraneStackReader("input-test.txt")
test_data = test_reader.read()

reader = CraneStackReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def display_stack(stack: Dict[int, deque]) -> str:
    """
    Given a stack, display it.
    E.g.

     123
     NDP
     ZC
      M

    Warning: Order is the same as shown on AOC, just packed from above instead of bellow
    """
    all_empty = all(map(lambda x: not len(x), stack.values()))
    lines = [" " + "".join(map(str, sorted(stack.keys())))]
    while not all_empty:
        line = " " * len(stack)
        for index in sorted(stack.keys()):
            if len(stack[index]):
                line = line[:index] + f"{stack[index].popleft()}" + line[index + 1 :]
        lines.append(line)
        all_empty = all(map(lambda x: not len(x), stack.values()))

    return "\n".join(lines)


def run(stack: Dict[int, deque], instructions: List[Instruction]):
    """
    Given a stack and instructions, run the process for step 1
    """
    for index, instruction in enumerate(instructions):
        print(f"index {index} {instruction}")
        for _ in range(instruction.number):
            value = stack[instruction.origin].popleft()
            stack[instruction.destination].appendleft(value)
        print(f"index {index}\n{display_stack(deepcopy(stack))}\n#######\n")
    return stack


def run2(stack: Dict[int, deque], instructions: List[Instruction]):
    """
    Given a stack and instructions, run the process for step 2
    """
    for index, instruction in enumerate(instructions):
        print(f"index {index} {instruction}")
        temp = []
        for _ in range(instruction.number):
            value = stack[instruction.origin].popleft()
            temp.append(value)
        for item in reversed(temp):
            stack[instruction.destination].appendleft(item)
        print(f"index {index}\n{display_stack(deepcopy(stack))}\n#######\n")
    return stack


for data_source_name, data_source in data_sources:
    print(f"Day 1 - Result 1 - {data_source_name}")
    stack, instructions = deepcopy(data_source)
    print(f"stack before:\n{display_stack(deepcopy(stack))}")
    processed_stack = run(stack, instructions)
    print(f"stack after:\n{display_stack(processed_stack)}")

    print(f"Day 1 - Result 2 - {data_source_name}")
    stack, instructions = data_source
    print(f"stack before:\n{display_stack(deepcopy(stack))}")
    processed_stack = run2(stack, instructions)
    print(f"stack after:\n{display_stack(processed_stack)}")
