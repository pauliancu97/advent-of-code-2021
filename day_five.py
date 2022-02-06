from __future__ import annotations
from dataclasses import dataclass
from re import Pattern, compile as regex_compile
from typing import ClassVar, Optional
from matrix import Matrix
from utils import read_lines


@dataclass(frozen=True)
class Point:
    row: int
    col: int

@dataclass(frozen=True)
class Line:
    start: Point
    end: Point

    line_regex: ClassVar[Pattern[str]] = regex_compile(r'(\d+),(\d+) -> (\d+),(\d+)')

    def is_horizontal(self) -> bool:
        return self.start.row == self.end.row

    def is_vertical(self) -> bool:
        return self.start.col == self.end.col

    def is_diagonal(self) -> bool:
        return not (self.is_horizontal() or self.is_vertical())

    def place_on_matrix(self, matrix: Matrix[int]) -> None:
        if self.is_horizontal():
            start_col = min(self.start.col, self.end.col)
            end_col = max(self.start.col, self.end.col) + 1
            row = self.start.row
            for col in range(start_col, end_col):
                matrix[row, col] += 1
        elif self.is_vertical():
            start_row = min(self.start.row, self.end.row)
            end_row = max(self.start.row, self.end.row) + 1
            col = self.start.col
            for row in range(start_row, end_row):
                matrix[row, col] += 1
        else:
            num_steps = abs(self.start.col - self.end.col) + 1
            row_offset = 1 if self.end.row > self.start.row else -1
            col_offset = 1 if self.end.col > self.start.col else -1
            for step in range(0, num_steps):
                row = self.start.row + step * row_offset
                col = self.start.col + step * col_offset
                matrix[row, col] += 1

    @staticmethod
    def from_string(string: str) -> Optional[Line]:
        match = Line.line_regex.match(string)
        if match is not None:
            start_col = int(match.group(1))
            start_row = int(match.group(2))
            end_col = int(match.group(3))
            end_row = int(match.group(4))
            return Line(Point(start_row, start_col), Point(end_row, end_col))
        return None


def get_valid_lines(strings: list[str]) -> list[Line]:
    return [opt_line for opt_line in [Line.from_string(string) for string in strings] if (opt_line is not None) and (not opt_line.is_diagonal())]


def get_lines(strings: list[str]) -> list[Line]:
    return [opt_line for opt_line in [Line.from_string(string) for string in strings] if opt_line is not None]


def get_initial_matrix(lines: list[Line]) -> Matrix[int]:
    rows = max(max(line.start.row, line.end.row) for line in lines) + 1
    cols = max(max(line.start.col, line.end.col) for line in lines) + 1
    return Matrix.with_default(rows, cols, 0)


def get_populated_map(lines: list[Line]) -> Matrix[int]:
    map = get_initial_matrix(lines)
    for line in lines:
        line.place_on_matrix(map)
    return map


def get_num_cells_multiple_lines(map: Matrix[int]) -> int:
    result = 0
    for row in range(0, map.rows):
        for col in range(0, map.cols):
            if map[row, col] >= 2:
                result += 1
    return result


def solve_part_one() -> None:
    strings = read_lines('day_five.txt')
    lines = get_valid_lines(strings)
    map = get_populated_map(lines)
    answer = get_num_cells_multiple_lines(map)
    print(answer)


def solve_part_two() -> None:
    strings = read_lines('day_five.txt')
    lines = get_lines(strings)
    map = get_populated_map(lines)
    answer = get_num_cells_multiple_lines(map)
    print(answer)


if __name__ == '__main__':
    solve_part_two()