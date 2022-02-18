from __future__ import annotations
from typing import TypeVar, Generic


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