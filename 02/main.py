"""
Could probably be way more smart about this, but bruteforce copy paste it is
"""
from enum import Enum
from typing import List

from rich import print

from utils.readers import OneColumnFileReader


class MoveEnum(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class ResultEnum(Enum):
    LOSE = 1
    DRAW = 2
    WIN = 3


def to_move(move:str) -> MoveEnum:
    if move in ["A", "X"]:
        return MoveEnum.ROCK
    if move in ["B", "Y"]:
        return MoveEnum.PAPER
    if move in ["C", "Z"]:
        return MoveEnum.SCISSORS


def to_result(result:str) -> ResultEnum:
    if result in ["X"]:
        return ResultEnum.LOSE
    if result in ["Y"]:
        return ResultEnum.DRAW
    if result in ["Z"]:
        return ResultEnum.WIN


class StrategyGuideReader(OneColumnFileReader):
    """
    Implementation of a rock paper scissors strategy

    E.g.

    A Y
    B X
    C Z

    ->
    [[R, P], [P, R], [S S]]
    """

    def read(self, *args) -> List[List]:
        """
        Implementation of a one column space aware data file read function
        """
        data = super(StrategyGuideReader, self).read()
        result = []
        for line in data:
            opponent, me = line.split(" ")
            opponent = to_move(opponent)
            me = to_result(me)
            result.append([opponent, me])

        return result


test_reader = StrategyGuideReader("input-test.txt")
test_data = test_reader.read()

reader = StrategyGuideReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data)
)


def compute_move_score(opponent: MoveEnum, me: MoveEnum) -> int:
    """
    Given two move, return the score
    """
    match opponent:
        case MoveEnum.ROCK:
            match me:
                case MoveEnum.ROCK:
                    return 1 + 3
                case MoveEnum.PAPER:
                    return 2 + 6
                case MoveEnum.SCISSORS:
                    return 3 + 0
        case MoveEnum.PAPER:
            match me:
                case MoveEnum.ROCK:
                    return 1 + 0
                case MoveEnum.PAPER:
                    return 2 + 3
                case MoveEnum.SCISSORS:
                    return 3 + 6
        case MoveEnum.SCISSORS:
            match me:
                case MoveEnum.ROCK:
                    return 1 + 6
                case MoveEnum.PAPER:
                    return 2 + 0
                case MoveEnum.SCISSORS:
                    return 3 + 3


def find_move_from_result(opponent: MoveEnum, me: ResultEnum):
    """
    Given the opponent move and the wished result, return the move to do
    """
    match opponent:
        case MoveEnum.ROCK:
            match me:
                case ResultEnum.LOSE:
                    return MoveEnum.SCISSORS
                case ResultEnum.DRAW:
                    return MoveEnum.ROCK
                case ResultEnum.WIN:
                    return MoveEnum.PAPER
        case MoveEnum.PAPER:
            match me:
                case ResultEnum.LOSE:
                    return MoveEnum.ROCK
                case ResultEnum.DRAW:
                    return MoveEnum.PAPER
                case ResultEnum.WIN:
                    return MoveEnum.SCISSORS
        case MoveEnum.SCISSORS:
            match me:
                case ResultEnum.LOSE:
                    return MoveEnum.PAPER
                case ResultEnum.DRAW:
                    return MoveEnum.SCISSORS
                case ResultEnum.WIN:
                    return MoveEnum.ROCK


def compute_scores(data: List[List]) -> int:
    """
    Given a list of opponent moves and results, compute the final score.
    """
    total_score = 0
    for move in data:
        opponent_move = move[0]
        result = move[1]
        my_move = find_move_from_result(opponent_move, result)
        score = compute_move_score(opponent_move, my_move)

        print(f"Op: {opponent_move}, res:{result}, me:{my_move} -> score {score}")

        total_score += score
    return total_score

for data_source_name, data_source in data_sources:
    # print(
    #     f"Day 1 - Result 1 - {data_source_name}: {compute_scores(data_source)}"
    # )
    print(
        f"Day 1 - Result 2 - {data_source_name}: {compute_scores(data_source)}"
    )

