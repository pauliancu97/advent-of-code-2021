from enum import IntEnum
from dataclasses import dataclass, replace
import re
from typing import Optional

from utils import read_lines


FORWARD_INSTR_REG_EX = re.compile(r'forward (\d+)')
UP_INSTR_REG_EX = re.compile(r'up (\d+)')
DOWN_INSTR_REG_EX = re.compile(r'down (\d+)')


class InstructionType(IntEnum):
    FORWARD = 1
    DOWN = 2
    UP = 3


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class SubmarineState:
    position: Position = Position(0, 0)
    aim: int = 0


@dataclass(frozen=True)
class Instruction:
    instruction_type: InstructionType
    value: int

    def get_next_state(self, state: SubmarineState) -> SubmarineState:
        match self.instruction_type:
            case InstructionType.FORWARD:
                return replace(
                    state, 
                    position=replace(
                        state.position, 
                        y=state.position.y + state.aim * self.value, 
                        x = state.position.x + self.value))
            case InstructionType.DOWN:
                return replace(state, aim=state.aim + self.value)
            case InstructionType.UP:
                return replace(state, aim=state.aim - self.value)


def get_final_position(instructions: list[Instruction]) -> Position:
    result = Position(x=0, y=0)
    for instruction in instructions:
        match instruction.instruction_type:
            case InstructionType.FORWARD:
                result = replace(result, x=result.x + instruction.value)
            case InstructionType.UP:
                result = replace(result, y=result.y - instruction.value)
            case InstructionType.DOWN:
                result = replace(result, y=result.y + instruction.value)
    return result


def get_final_submarine_position(instructions: list[Instruction]) -> Position:
    state = SubmarineState()
    for instruction in instructions:
        state = instruction.get_next_state(state)
    return state.position


def get_instruction(line: str) -> Optional[Instruction]:
    match = FORWARD_INSTR_REG_EX.match(line)
    if match:
        return Instruction(instruction_type=InstructionType.FORWARD, value=int(match.group(1)))
    match = UP_INSTR_REG_EX.match(line)
    if match:
        return Instruction(instruction_type=InstructionType.UP, value=int(match.group(1)))
    match = DOWN_INSTR_REG_EX.match(line)
    if match:
        return Instruction(instruction_type=InstructionType.DOWN, value=int(match.group(1)))
    return None

def get_instrunctions(lines: list[str]) -> list[Instruction]:
    return [opt_instr for opt_instr in [get_instruction(line) for line in lines] if opt_instr]


def solve_part_one() -> None:
    lines = read_lines('day_two.txt')
    instructions = get_instrunctions(lines)
    point = get_final_position(instructions)
    answer = point.x * point.y
    print(answer)


def solve_part_two() -> None:
    lines = read_lines('day_two.txt')
    instructions = get_instrunctions(lines)
    point = get_final_submarine_position(instructions)
    answer = point.x * point.y
    print(answer)


if __name__ == '__main__':
    solve_part_two()