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

    @property
    def rows(self) -> int:
        return len(self._values)

    @property
    def cols(self) -> int:
        if len(self._values) == 0:
            return 0
        return len(self._values[0])