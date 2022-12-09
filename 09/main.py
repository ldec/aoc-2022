from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Tuple

from utils.out import print
from utils.readers import OneColumnFileReader


class Direction:
    pass


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

    @classmethod
    def from_string(cls, data: str) -> Direction:
        """
        Given a direction string, return the direction
        """
        match data:
            case "R":
                return cls.RIGHT
            case "L":
                return cls.LEFT
            case "U":
                return cls.UP
            case "D":
                return cls.DOWN


class Position:
    pass


@dataclass
class Position:
    x: int
    y: int

    def to_tuple(self):
        """
        Return a tuple (x,y)
        """
        return self.x, self.y

    def is_touching(self, position: Position):
        """
        Given another position, check if it's touching
        """
        if self.x == position.x and self.y == position.y:
            return True

        return abs(position.x - self.x) <= 1 and abs(position.y - self.y) <= 1


@dataclass
class Rope:
    head: Position
    knots: List[Position]
    tail: Position
    previous_tail_positions: Set[Tuple[int, int]]

    def follow(self, head: Position, tail: Position, record: bool):
        """
        Given a head and tail, if the tail is not touching the head, update the tail
        to follow the head according to the rules
        """
        if tail.is_touching(head):
            return

        x_direction = head.x - tail.x
        y_direction = head.y - tail.y

        # Move non diagonally
        if y_direction == 0:
            if x_direction < 0:
                tail.x += -1
            else:
                tail.x += 1

        if x_direction == 0:
            if y_direction < 0:
                tail.y += -1
            else:
                tail.y += 1

        # Move diagonally
        if x_direction < 0 and y_direction < 0:
            tail.x += -1
            tail.y += -1

        if x_direction < 0 and y_direction > 0:
            tail.x += -1
            tail.y += 1

        if x_direction > 0 and y_direction < 0:
            tail.x += 1
            tail.y += -1

        if x_direction > 0 and y_direction > 0:
            tail.x += 1
            tail.y += 1

        if record:
            self.previous_tail_positions.add(tail.to_tuple())

    def play_move(self, direction: Direction, count: int):
        """
        Given a direction and a count, play the move
        """
        for _ in range(count):
            match direction:
                case Direction.RIGHT:
                    self.move_head(self.head.x + 1, self.head.y)
                case Direction.LEFT:
                    self.move_head(self.head.x - 1, self.head.y)
                case Direction.UP:
                    self.move_head(self.head.x, self.head.y + 1)
                case Direction.DOWN:
                    self.move_head(self.head.x, self.head.y - 1)

    def follow_knots(self):
        """
        Ensure each knot are following the head
        """
        for index, knot in enumerate(self.knots):
            if index == 0:
                head = self.head
            else:
                head = self.knots[index - 1]
            self.follow(head, knot, record=False)

    def move_head(self, x: int, y: int):
        """
        Move the head to the given x and y coordinates, ensure that knots and the tail
        move as well
        """
        self.head.x = x
        self.head.y = y

        self.follow_knots()

        knot = self.head
        if self.knots:
            knot = self.knots[-1]
        self.follow(knot, self.tail, record=True)


class MoveReader(OneColumnFileReader):
    """
    Implementation of a move reader

    E.g.

    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2
    """

    def read(self, *args):
        data = super(MoveReader, self).read()
        result = []
        for row in data:
            raw_direction, raw_count = row.split(" ")
            result.append(
                [
                    Direction.from_string(raw_direction),
                    int(raw_count),
                ]
            )

        return result


def play1(moves: List):
    """
    Play the move with a rope of length 2
    """
    rope = Rope(Position(0, 0), [], Position(0, 0), {(0, 0)})

    for direction, count in moves:
        rope.play_move(direction, count)

    return rope


def play2(moves: List):
    """
    Play the move with a rope of length 10 (head, 9 knots, tail)
    """
    knots = [
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
        Position(0, 0),
    ]
    rope = Rope(Position(0, 0), knots, Position(0, 0), {(0, 0)})

    for direction, count in moves:
        rope.play_move(direction, count)

    return rope


def main():
    test_reader = MoveReader("input-test.txt")
    test_data = test_reader.read()

    reader = MoveReader("input.txt")
    prod_data = reader.read()

    data_sources = (
        ("Test data", test_data),
        ("Prod data", prod_data),
    )

    for data_source_name, data_source in data_sources:
        result = play1(data_source)
        result2 = play2(data_source)
        print(
            f"Day 1 - Result 1 - {data_source_name}: {len(result.previous_tail_positions)}"
        )
        print(
            f"Day 1 - Result 1 - {data_source_name}: {len(result2.previous_tail_positions)}"
        )


if __name__ == "__main__":
    main()
