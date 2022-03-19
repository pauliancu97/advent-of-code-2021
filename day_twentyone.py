from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import functools


DICES = [(d1, d2, d3) for d1 in range(1, 4) for d2 in range(1, 4) for d3 in range(1, 4)]

@dataclass(frozen=True)
class Player:
    position: int
    score: int = 0

    def get_updated(self, dices: tuple[int, int, int]) -> Player:
        d1, d2, d3 = dices
        updated_position = (self.position + d1 % 10 + d2 % 10 + d3 %10) % 10
        updated_score = self.score + updated_position + 1
        return Player(updated_position, updated_score)


class Turn(Enum):
    FIRST_PLAYER = 1
    SECOND_PLAYER = 2

    def get_next_turn(self: Turn) -> Turn:
        match self:
            case Turn.FIRST_PLAYER:
                return Turn.SECOND_PLAYER
            case Turn.SECOND_PLAYER:
                return Turn.FIRST_PLAYER


def get_answer(first_player_position: int, second_player_position: int) -> int:
    dice = 1
    turn = 0
    first_player_score = 0
    second_player_score = 0
    while first_player_score < 1000 and second_player_score < 1000:
        if turn % 2 == 0:
            first_player_position = (first_player_position + dice % 10 + (dice + 1) % 10 + (dice + 2) % 10) % 10
            first_player_score += (first_player_position + 1)
        else:
            second_player_position = (second_player_position + dice % 10 + (dice + 1) % 10 + (dice + 2) % 10) % 10
            second_player_score += (second_player_position + 1)
        turn += 1
        dice += 3
    losing_player_score = first_player_score if first_player_score < 100 else second_player_score
    return losing_player_score * turn * 3


@functools.cache
def get_game_result_helper(first: Player, second: Player, turn: Turn) -> tuple[int, int]:
    if first.score >= 21:
        return 1, 0
    elif second.score >= 21:
        return 0, 1
    else:
        first_player_wins = 0
        second_player_wins = 0
        for dice in DICES:
            match turn:
                case Turn.FIRST_PLAYER:
                    obtained_first_player_winds, obtained_second_player_wins = get_game_result_helper(first.get_updated(dice), second, turn.get_next_turn())
                    first_player_wins += obtained_first_player_winds
                    second_player_wins += obtained_second_player_wins
                case Turn.SECOND_PLAYER:
                    obtained_first_player_winds, obtained_second_player_wins = get_game_result_helper(first, second.get_updated(dice), turn.get_next_turn())
                    first_player_wins += obtained_first_player_winds
                    second_player_wins += obtained_second_player_wins
        return first_player_wins, second_player_wins


def get_game_result(first_player_position: int, second_player_position: int) -> int:
    first = Player(first_player_position, 0)
    second = Player(second_player_position, 0)
    first_wins, second_wins = get_game_result_helper(first, second, Turn.FIRST_PLAYER)
    return max(first_wins, second_wins)


def solve_part_one() -> None:
    print(get_answer(4, 7))


def solve_part_two() -> None:
    print(get_game_result(4, 7))


if __name__ == '__main__':
    solve_part_two()