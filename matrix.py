from __future__ import annotations
from typing import Optional, TypeVar, Generic
from copy import deepcopy


T = TypeVar('T')


class Matrix(Generic[T]):
    
    def __init__(self, values: list[list[T]]) -> None:
        super().__init__()
        self._values = values

    def __getitem__(self, coordinate: tuple[int, int]) -> T:
        row, col = coordinate
        return self._values[row][col]

    def __setitem__(self, coordinate: tuple[int, int], value: T) -> None:
        row, col = coordinate
        self._values[row][col] = value

    def __contains__(self, value: T) -> bool:
        return any(value in row for row in self._values)

    def has_coordinates(self, coordinates: tuple[int, int]) -> bool:
        row, col = coordinates
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols

    def __str__(self) -> str:
        string = ''
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                string += str(self[row, col])
            string += '\n'
        return string

    def __repr__(self) -> str:
        string = ''
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                string += str(self[row, col])
            string += '\n'
        return string

    def reversed_rows(self) -> Matrix[T]:
        result = deepcopy(self)
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                result[row, col] = self[self.rows - row - 1, col]
        return result

    def reversed_cols(self) -> Matrix[T]:
        result = deepcopy(self)
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                result[row, col] = self[row , self.cols - col - 1]
        return result

    def splitted_horizontally(self, start_row: int, end_row: Optional[int] = None) -> Matrix[T]:
        actual_end_row = self.rows if end_row is None else end_row
        splitted_rows = actual_end_row - start_row
        result = Matrix[T].with_default(splitted_rows, self.cols, self[0, 0])
        for row in range(0, result.rows):
            for col in range(0, result.cols):
                result[row, col] = self[row + start_row, col]
        return result

    def splitted_vertically(self, start_col: int, end_col: Optional[int] = None) -> Matrix[T]:
        actual_end_col = self.cols if end_col is None else end_col
        splitted_cols = actual_end_col - start_col
        result = Matrix[T].with_default(self.rows, splitted_cols, self[0, 0])
        for row in range(0, result.rows):
            for col in range(0, result.cols):
                result[row, col] = self[row, col + start_col]
        return result

    @property
    def rows(self) -> int:
        return len(self._values)

    @property
    def cols(self) -> int:
        if len(self._values) == 0:
            return 0
        return len(self._values[0])

    @classmethod
    def with_default(cls, rows: int, cols: int, default: T) -> Matrix[T]:
        list_matrix = [[default for _ in range(0, cols)] for _ in range(0, rows)]
        return cls(list_matrix)