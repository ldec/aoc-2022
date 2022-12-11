from collections import Counter
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Optional

from math import floor, lcm


@dataclass
class Monkey:
    items: Deque[int]
    operation: Callable
    test_value: int
    test_true: int
    test_false: int

    def test(self, x: int):
        return x % self.test_value == 0


def test_monkeys():
    monkey_0_queue = deque()
    monkey_1_queue = deque()
    monkey_2_queue = deque()
    monkey_3_queue = deque()

    for i in [79, 98]:
        monkey_0_queue.append(i)

    for i in [54, 65, 75, 74]:
        monkey_1_queue.append(i)

    for i in [79, 60, 97]:
        monkey_2_queue.append(i)

    for i in [74]:
        monkey_3_queue.append(i)

    return {
        0: Monkey(
            items=monkey_0_queue,
            operation=lambda x: x * 19,
            test_value=23,
            test_true=2,
            test_false=3,
        ),
        1: Monkey(
            items=monkey_1_queue,
            operation=lambda x: x + 6,
            test_value=19,
            test_true=2,
            test_false=0,
        ),
        2: Monkey(
            items=monkey_2_queue,
            operation=lambda x: x * x,
            test_value=13,
            test_true=1,
            test_false=3,
        ),
        3: Monkey(
            items=monkey_3_queue,
            operation=lambda x: x + 3,
            test_value=17,
            test_true=0,
            test_false=1,
        ),
    }


def prod_monkeys():
    monkey_0_queue = deque()
    monkey_1_queue = deque()
    monkey_2_queue = deque()
    monkey_3_queue = deque()
    monkey_4_queue = deque()
    monkey_5_queue = deque()
    monkey_6_queue = deque()
    monkey_7_queue = deque()

    for i in [78, 53, 89, 51, 52, 59, 58, 85]:
        monkey_0_queue.append(i)

    for i in [64]:
        monkey_1_queue.append(i)

    for i in [71, 93, 65, 82]:
        monkey_2_queue.append(i)

    for i in [67, 73, 95, 75, 56, 74]:
        monkey_3_queue.append(i)

    for i in [85, 91, 90]:
        monkey_4_queue.append(i)

    for i in [67, 96, 69, 55, 70, 83, 62]:
        monkey_5_queue.append(i)

    for i in [53, 86, 98, 70, 64]:
        monkey_6_queue.append(i)

    for i in [88, 64]:
        monkey_7_queue.append(i)

    return {
        0: Monkey(
            items=monkey_0_queue,
            operation=lambda x: x * 3,
            test_value=5,
            test_true=2,
            test_false=7,
        ),
        1: Monkey(
            items=monkey_1_queue,
            operation=lambda x: x + 7,
            test_value=2,
            test_true=3,
            test_false=6,
        ),
        2: Monkey(
            items=monkey_2_queue,
            operation=lambda x: x + 5,
            test_value=13,
            test_true=5,
            test_false=4,
        ),
        3: Monkey(
            items=monkey_3_queue,
            operation=lambda x: x + 8,
            test_value=19,
            test_true=6,
            test_false=0,
        ),
        4: Monkey(
            items=monkey_4_queue,
            operation=lambda x: x + 4,
            test_value=11,
            test_true=3,
            test_false=1,
        ),
        5: Monkey(
            items=monkey_5_queue,
            operation=lambda x: x * 2,
            test_value=3,
            test_true=4,
            test_false=1,
        ),
        6: Monkey(
            items=monkey_6_queue,
            operation=lambda x: x + 6,
            test_value=7,
            test_true=7,
            test_false=0,
        ),
        7: Monkey(
            items=monkey_7_queue,
            operation=lambda x: x * x,
            test_value=17,
            test_true=2,
            test_false=5,
        ),
    }


def do_round(
    monkeys: Dict[int, Monkey], monkey_activity: Counter, worry_division: Callable
):
    for monkey_id, monkey in monkeys.items():
        if not len(monkey.items):
            continue

        while len(monkey.items):
            monkey_activity[monkey_id] += 1

            item = monkey.items.popleft()

            item = monkey.operation(item)
            item = worry_division(item)

            target = monkey.test_true
            if not monkey.test(item):
                target = monkey.test_false
            monkeys[target].items.append(item)

    return monkeys


def process(
    monkeys: Dict[int, Monkey], worry_division: Optional[Callable], rounds: int
):
    if worry_division is None:
        base = lcm(*(monkey.test_value for monkey in monkeys.values()))
        worry_division = lambda x: x % base

    monkey_activity = Counter()
    for _ in range(1, rounds + 1):
        monkeys = do_round(monkeys, monkey_activity, worry_division=worry_division)

    top_two = monkey_activity.most_common(2)
    return top_two[0][1] * top_two[1][1]


def main():
    data_sources = (
        ("Test data", test_monkeys()),
        ("Prod data", prod_monkeys()),
    )

    for data_source_name, data_source in data_sources:
        print(
            f"Day 11 - Result 1 - {data_source_name}: {process(deepcopy(data_source), worry_division=lambda x: floor(x/3), rounds=20)}"
        )
        print(
            f"Day 11 - Result 2 - {data_source_name}: {process(deepcopy(data_source), worry_division=None, rounds=10000)}"
        )


if __name__ == "__main__":
    main()
