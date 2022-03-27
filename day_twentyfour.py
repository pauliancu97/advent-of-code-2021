from dataclasses import dataclass
from enum import Enum
from re import compile as re_compile
from typing import Optional
from utils import read_lines
from copy import deepcopy


REGEX_INPUT = re_compile(r'inp ([wxyz])')
REGEX_ADDITION = re_compile(r'add ([wxyz]) ([wxyz]|[-+]?\d+)')
REGEX_MULTIPLICATION = re_compile(r'mul ([wxyz]) ([wxyz]|[-+]?\d+)')
REGEX_DIVISION = re_compile(r'div ([wxyz]) ([wxyz]|[-+]?\d+)')
REGEX_MODULO = re_compile(r'mod ([wxyz]) ([wxyz]|[-+]?\d+)')
REGEX_EQUAL = re_compile(r'eql ([wxyz]) ([wxyz]|[-+]?\d+)')
MODEL_NUMBER_LENGTH = 14


class Register(Enum):
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'

    @staticmethod
    def is_register(string: str) -> bool:
        register_values = [register.value for register in Register]
        return string in register_values


@dataclass
class Input:
    register: Register


@dataclass
class Addition:
    first: Register
    second: int | Register


@dataclass
class Multiplication:
    first: Register
    second: int | Register


@dataclass
class Division:
    first: Register
    second: int | Register


@dataclass
class Modulo:
    first: Register
    second: int | Register


@dataclass
class Equal:
    first: Register
    second: int | Register


Instruction = Input | Addition | Multiplication | Division | Modulo | Equal
Program = list[Instruction]


def get_instruction(string: str) -> Optional[Instruction]:
    match = REGEX_INPUT.match(string)
    if match:
        register = Register(match.group(1))
        return Input(register)
    match = REGEX_ADDITION.match(string)
    if match:
        first = Register(match.group(1))
        second_str = match.group(2)
        if not Register.is_register(second_str):
            return Addition(first, int(second_str))
        else:
            return Addition(first, Register(second_str))
    match = REGEX_MULTIPLICATION.match(string)
    if match:
        first = Register(match.group(1))
        second_str = match.group(2)
        if not Register.is_register(second_str):
            return Multiplication(first, int(second_str))
        else:
            return Multiplication(first, Register(second_str))
    match = REGEX_DIVISION.match(string)
    if match:
        first = Register(match.group(1))
        second_str = match.group(2)
        if not Register.is_register(second_str):
            return Division(first, int(second_str))
        else:
            return Division(first, Register(second_str))
    match = REGEX_MODULO.match(string)
    if match:
        first = Register(match.group(1))
        second_str = match.group(2)
        if not Register.is_register(second_str):
            return Modulo(first, int(second_str))
        else:
            return Modulo(first, Register(second_str))
    match = REGEX_EQUAL.match(string)
    if match:
        first = Register(match.group(1))
        second_str = match.group(2)
        if not Register.is_register(second_str):
            return Equal(first, int(second_str))
        else:
            return Equal(first, Register(second_str))
    return None


def read_program(path: str) -> Program:
    strings = read_lines(path)
    opt_instructions = [get_instruction(string) for string in strings]
    return [opt_instr for opt_instr in opt_instructions if opt_instr]


class APU:

    def __init__(self, program: Program):
        self._registers = { register: 0 for register in Register}
        self._program = program

    def _execute_instruction(self, input: int) -> None:
        instruction = self._program.pop(0)
        match instruction:
            case Input(register):
                self._registers[register] = input
            case Addition(first, second):
                if isinstance(second, int):
                    self._registers[first] += second
                else:
                    self._registers[first] += self._registers[second]
            case Multiplication(first, second):
                if isinstance(second, int):
                    self._registers[first] *= second
                else:
                    self._registers[first] *= self._registers[second]
            case Division(first, second):
                if isinstance(second, int):
                    self._registers[first] //= second
                else:
                    self._registers[first] //= self._registers[second]
            case Modulo(first, second):
                if isinstance(second, int):
                    self._registers[first] %= second
                else:
                    self._registers[first] %= self._registers[second]
            case Equal(first, second):
                if isinstance(second, int):
                    self._registers[first] = 1 if self._registers[first] == second else 0
                else:
                    self._registers[first] = 1 if self._registers[first] == self._registers[second] else 0

    def execute(self, input: int) -> None:
        self._execute_instruction(input)
        while len(self._program) != 0 and not isinstance(self._program[0], Input):
            self._execute_instruction(input)

    def set_register(self, register: Register, value: int) -> None:
        self._registers[register] = value

    def get_register(self, register: Register) -> int:
        return self._registers[register]


def get_set_digits(apu: APU) -> list[Optional[int]]:
    set_digits: list[Optional[int]] = []
    for index in range(0, MODEL_NUMBER_LENGTH):
        if index == 0:
            apu.execute(9)
            set_digits.append(None)
        else:
            chosen_digit: Optional[int] = None
            for digit in reversed(range(1, 10)):
                current_apu = deepcopy(apu)
                z = current_apu.get_register(Register.Z)
                current_apu.execute(digit)
                if current_apu.get_register(Register.Z) < z:
                    chosen_digit = digit
                    break
            set_digits.append(chosen_digit)
            apu.execute(9)
    return set_digits


def search_biggest_valid_model_number(model_number: list[int], set_digits: list[Optional[int]], apu: APU) -> Optional[list[int]]:
    if len(model_number) + 1 == MODEL_NUMBER_LENGTH:
        set_digit = set_digits[len(model_number)]
        if set_digit:
            current_apu = deepcopy(apu)
            current_apu.execute(set_digit)
            if current_apu.get_register(Register.Z) == 0:
                return model_number + [set_digit]
            else:
                return None
        else:
            for digit in reversed(range(1, 10)):
                current_apu = deepcopy(apu)
                current_apu.execute(digit)
                if current_apu.get_register(Register.Z) == 0:
                    return model_number + [digit]
            return None
    else:
        set_digit = set_digits[len(model_number)]
        if set_digit:
            current_apu = deepcopy(apu)
            current_apu.execute(set_digit)
            return search_biggest_valid_model_number(model_number + [set_digit], set_digits, current_apu)
        else:
            for digit in reversed(range(1, 10)):
                current_apu = deepcopy(apu)
                current_apu.execute(digit)
                result = search_biggest_valid_model_number(model_number + [digit], set_digits, current_apu)
                if result:
                    return result
            return None


def get_biggest_valid_model_number(program: Program) -> Optional[str]:
    set_digits = get_set_digits(APU(deepcopy(program)))
    result = search_biggest_valid_model_number([], set_digits, APU(deepcopy(program)))
    if result:
        return ''.join([str(digit) for digit in result])


def solve_part_one() -> None:
    program = read_program('day_twentyfour.txt')
    print(get_biggest_valid_model_number(program))


if __name__ == '__main__':
    solve_part_one()
    