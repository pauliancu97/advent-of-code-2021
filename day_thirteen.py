from matrix import Matrix
from dataclasses import dataclass
from functools import reduce
from typing import Optional
from re import compile as regex_compile
from utils import read_lines


COORDINATE_REGEX = regex_compile(r'(\d+),(\d+)')
FOLD_UP_REGEX = regex_compile(r'fold along y=(\d+)')
FOLD_LEFT_REGEX = regex_compile(r'fold along x=(\d+)')


@dataclass(frozen=True)
class FoldUp:
    row: int


@dataclass(frozen=True)
class FoldLeft:
    col: int


FoldInstruction = FoldUp | FoldLeft


def get_coordinate(line: str) -> Optional[tuple[int, int]]:
    match = COORDINATE_REGEX.match(line)
    if match:
        col, row = match.group(1, 2)
        return int(row), int(col)


def get_paper(coordinates: list[tuple[int, int]]) -> Matrix[bool]:
    rows = max([coordinate[0] for coordinate in coordinates]) + 1
    cols = max([coordinate[1] for coordinate in coordinates]) + 1
    result = Matrix[bool].with_default(rows, cols, False)
    for row, col in coordinates:
        result[row, col] = True
    return result


def get_coordinates(lines: list[str]) -> list[tuple[int, int]]:
    return [opt_coord for opt_coord in [get_coordinate(line) for line in lines] if opt_coord]


def get_after_fold_instruction(matrix: Matrix[bool], fold_instruction: FoldInstruction) -> Matrix[bool]:
    match fold_instruction:
        case FoldUp(row):
            return get_folded_up(matrix, row)
        case FoldLeft(col):
            return get_folded_left(matrix, col)


def get_after_fold_instructions(matrix: Matrix[bool], fold_instructions: list[FoldInstruction]) -> Matrix[bool]:
    return reduce(lambda acc, instruction: get_after_fold_instruction(acc, instruction), fold_instructions, initial=matrix)


def get_folded_up(matrix: Matrix[bool], start_row: int) -> Matrix[bool]:
    upper_part = matrix.splitted_horizontally(0, start_row)
    bottom_part = matrix.splitted_horizontally(start_row + 1).reversed_rows()
    upper_row_start = upper_part.rows - bottom_part.rows
    for row in range(0, bottom_part.rows):
        for col in range(0, bottom_part.cols):
            upper_part[upper_row_start + row, col] = upper_part[upper_row_start + row, col] or bottom_part[row, col]
    return upper_part


def get_folded_left(matrix: Matrix[bool], start_col: int) -> Matrix[bool]:
    left_part = matrix.splitted_vertically(0, start_col)
    right_part = matrix.splitted_vertically(start_col + 1).reversed_cols()
    left_col_start = left_part.cols - right_part.cols
    for row in range(0, right_part.rows):
        for col in range(0, right_part.cols):
            left_part[row, left_col_start + col] = left_part[row, left_col_start + col] or right_part[row, col]
    return left_part


def get_instruction(line: str) -> Optional[FoldInstruction]:
    fold_up_match = FOLD_UP_REGEX.match(line)
    if fold_up_match:
        return FoldUp(int(fold_up_match.group(1)))
    fold_left_match = FOLD_LEFT_REGEX.match(line)
    if fold_left_match:
        return FoldLeft(int(fold_left_match.group(1)))


def get_instructions(lines: list[str]) -> list[FoldInstruction]:
    return [opt for opt in [get_instruction(line) for line in lines] if opt]


def get_input(path: str) -> tuple[Matrix[bool], list[FoldInstruction]]:
    lines = read_lines(path)
    separator_index = [index for index, line in enumerate(lines) if len(line) == 0][0]
    coordinates_lines = lines[:separator_index]
    instructions_lines = lines[separator_index + 1:]
    coordinates = get_coordinates(coordinates_lines)
    paper = get_paper(coordinates)
    fold_instructions = get_instructions(instructions_lines)
    return paper, fold_instructions


def get_num_dots(paper: Matrix[bool]) -> int:
    result = 0
    for row in range(0, paper.rows):
        for col in range(0, paper.cols):
            if paper[row, col]:
                result += 1
    return result


def solve_part_one():
    paper, fold_instructions = get_input('day_thirteen.txt')
    updated_paper = get_after_fold_instruction(paper, fold_instructions[0])
    print(get_num_dots(updated_paper))


if __name__ == '__main__':
    solve_part_one()
