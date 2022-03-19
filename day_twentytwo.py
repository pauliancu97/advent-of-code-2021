from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from re import compile, Pattern
from utils import read_lines


@dataclass(frozen=True)
class Range:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    REGEX: ClassVar[Pattern[str]] = compile(r'x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')

    @classmethod
    def from_string(cls, string: str) -> Range:
        match = Range.REGEX.match(string)
        if match:
            min_x, max_x, min_y, max_y, min_z, max_z = match.group(1, 2, 3, 4, 5, 6)
            return Range(int(min_x), int(max_x), int(min_y), int(max_y), int(min_z), int(max_z))
        raise ValueError


@dataclass(frozen=True)
class Instruction:
    value: bool
    range: Range

    ON_REGEX: ClassVar[Pattern[str]] = compile(r'on (.*)')
    OFF_REGEX: ClassVar[Pattern[str]] = compile(r'off (.*)')

    @classmethod
    def from_string(cls, string: str) -> Instruction:
        match = Instruction.ON_REGEX.match(string)
        if match:
            range_string = match.group(1)
            return Instruction(True, Range.from_string(range_string))
        match = Instruction.OFF_REGEX.match(string)
        if match:
            range_string = match.group(1)
            return Instruction(False, Range.from_string(range_string))
        raise ValueError


class Cube:

    def __init__(self, width: int, height: int, depth: int):
        self._width = width
        self._height = height
        self._depth = depth
        self._values = [[[False for _ in range(depth)] for _ in range(height)] for _ in range(width)]

    @classmethod
    def sized(cls, size: int) -> Cube:
        return cls(size, size, size)

    def __getitem__(self, coordinate: tuple[int, int, int]) -> bool:
        x, y, z = coordinate
        min_x = -((self._width - 1) // 2)
        min_y = -((self._height - 1) // 2)
        min_z = -((self._depth - 1) // 2)
        return self._values[x - min_x][y - min_y][z - min_z]

    def __setitem__(self, coordinate: tuple[int, int, int], value: bool) -> None:
        x, y, z = coordinate
        min_x = -((self._width - 1) // 2)
        min_y = -((self._height - 1) // 2)
        min_z = -((self._depth - 1) // 2)
        self._values[x - min_x][y - min_y][z - min_z] = value

    def __contains__(self, coordinate: tuple[int, int, int]) -> bool:
        min_x = -((self._width - 1) // 2)
        max_x = (self._width - 1) // 2
        min_y = -((self._height - 1) // 2)
        max_y = (self._height - 1) // 2
        min_z = -((self._depth - 1) // 2)
        max_z = (self._depth - 1) // 2
        x, y, z = coordinate
        return x >= min_x and x <= max_x and y >= min_y and y <= max_y and z >= min_z and z <= max_z

    def apply_instructions(self, instruction: Instruction) -> None:
        min_x = -((self._width - 1) // 2)
        max_x = (self._width - 1) // 2
        min_y = -((self._height - 1) // 2)
        max_y = (self._height - 1) // 2
        min_z = -((self._depth - 1) // 2)
        max_z = (self._depth - 1) // 2
        instruction_range_x = set(range(instruction.range.min_x, instruction.range.max_x + 1))
        instruction_range_y = set(range(instruction.range.min_y, instruction.range.max_y + 1))
        instruction_range_z = set(range(instruction.range.min_z, instruction.range.max_z + 1))
        cube_range_x = set(range(min_x, max_x + 1))
        cube_range_y = set(range(min_y, max_y + 1))
        cube_range_z = set(range(min_z, max_z + 1))
        range_x = instruction_range_x.intersection(cube_range_x)
        range_y = instruction_range_y.intersection(cube_range_y)
        range_z = instruction_range_z.intersection(cube_range_z)
        if len(range_x) == 0 or len(range_y) == 0 or len(range_z) == 0:
            return
        for x in range_x:
            for y in range_y:
                for z in range_z:
                    if (x, y, z) in self:
                        self[x, y, z] = instruction.value

    def get_num_on_cubes(self) -> int:
        result = 0
        for x in range(self._width):
            for y in range(self._height):
                for z in range(self._depth):
                    if self._values[x][y][z]:
                        result += 1
        return result
    

def get_instructions(path: str) -> list[Instruction]:
    lines = read_lines(path)
    return [Instruction.from_string(line) for line in lines]


def solve_part_one() -> None:
    instructions = get_instructions('day_twentytwo.txt')
    cube = Cube.sized(101)
    for instruction in instructions:
        cube.apply_instructions(instruction)
    print(cube.get_num_on_cubes())


if __name__ == '__main__':
    solve_part_one()