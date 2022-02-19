from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from utils import read_lines

class ParanDirection(Enum):
    LEFT = 1
    RIGHT = 2


class ParanType(Enum):
    NORMAL = 1
    SQUARE = 2
    CURLY = 3
    BRACKET = 4

    def get_score(self: ParanType) -> int:
        match self:
            case ParanType.NORMAL:
                return 3
            case ParanType.SQUARE:
                return 57
            case ParanType.CURLY:
                return 1197
            case ParanType.BRACKET:
                return 25137

    def get_completion_score(self: ParanType) -> int:
        match self:
            case ParanType.NORMAL:
                return 1
            case ParanType.SQUARE:
                return 2
            case ParanType.CURLY:
                return 3
            case ParanType.BRACKET:
                return 4


@dataclass(frozen=True)
class Paran:
    direction: ParanDirection
    type: ParanType


def get_paran(character: str) -> Optional[Paran]:
    match character:
        case '(':
            return Paran(ParanDirection.LEFT, ParanType.NORMAL)
        case ')':
            return Paran(ParanDirection.RIGHT, ParanType.NORMAL)
        case '[':
            return Paran(ParanDirection.LEFT, ParanType.SQUARE)
        case ']':
            return Paran(ParanDirection.RIGHT, ParanType.SQUARE)
        case '{':
            return Paran(ParanDirection.LEFT, ParanType.CURLY)
        case '}':
            return Paran(ParanDirection.RIGHT, ParanType.CURLY)
        case '<':
            return Paran(ParanDirection.LEFT, ParanType.BRACKET)
        case '>':
            return Paran(ParanDirection.RIGHT, ParanType.BRACKET)
        case _:
            return None


def get_parans(string: str) -> list[Paran]:
    res = [get_paran(character) for character in string]
    return [element for element in res if element]


def get_syntax_error_score_for_line(line: list[Paran]) -> int:
    result = 0
    stack: list[ParanType] = []
    for paran in line:
        match paran.direction:
            case ParanDirection.LEFT:
                stack.append(paran.type)
            case ParanDirection.RIGHT:
                last_paran_type = stack.pop()
                if last_paran_type != paran.type:
                    result = paran.type.get_score()
                    break
    return result


def get_completion(line: list[Paran]) -> list[ParanType]:
    stack: list[ParanType] = []
    for paran in line:
        match paran.direction:
            case ParanDirection.LEFT:
                stack.append(paran.type)
            case ParanDirection.RIGHT:
                stack.pop()
    return list(reversed(stack))


def get_completion_score(line: list[Paran]) -> int:
    completion = get_completion(line)
    result = 0
    for paran_type in completion:
        result = result * 5 + paran_type.get_completion_score()
    return result


def get_syntax_error_score(lines: list[list[Paran]]) -> int:
    return sum([get_syntax_error_score_for_line(line) for line in lines])


def get_lines(path: str) -> list[list[Paran]]:
    lines = read_lines(path)
    return [get_parans(line) for line in lines]


def solve_part_one() -> None:
    lines = get_lines('day_ten.txt')
    print(get_syntax_error_score(lines))

def solve_part_two() -> None:
    lines = get_lines('day_ten.txt')
    correct_lines = [line for line in lines if get_syntax_error_score_for_line(line) == 0]
    completion_scores = [get_completion_score(line) for line in correct_lines]
    completion_scores.sort()
    answer = completion_scores[len(completion_scores) // 2]
    print(answer)


if __name__ == '__main__':
    solve_part_two()