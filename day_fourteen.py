from re import compile as regex_compile
from typing import Optional
from utils import read_lines


REACTION_REGEX = regex_compile(r'([A-Z])([A-Z]) -> ([A-Z])')


ReactionsTable = dict[tuple[str, str], str]


def get_reaction(line: str) -> Optional[tuple[str, str, str]]:
    match = REACTION_REGEX.match(line)
    if match:
        return match.group(1, 2, 3)


def get_reaction_table(lines: list[str]) -> ReactionsTable:
    return { (reaction[0], reaction[1]): reaction[2] for reaction in [get_reaction(line) for line in lines] if reaction}


def get_polymer_after_iteration(polymer: str, reactions_table: ReactionsTable) -> str:
    pairs = zip(polymer[:-1], polymer[1:])
    return ''.join([first + reactions_table[first, second] for first, second in pairs]) + polymer[-1]


def get_polymer_after_iterations(polymer: str, reactions_table: ReactionsTable, num_iter: int) -> str:
    for _ in range(0, num_iter):
        polymer = get_polymer_after_iteration(polymer, reactions_table)
    return polymer


def get_answer(polymer: str) -> int:
    distinct_elements = set(polymer)
    counts = [polymer.count(element) for element in distinct_elements]
    return max(counts) - min(counts)


def get_input(path: str) -> tuple[str, ReactionsTable]:
    lines = read_lines(path)
    polymer = lines[0]
    reactions_table = get_reaction_table(lines[2:])
    return polymer, reactions_table


def solve_day_one() -> None:
    polymer, reactions_table = get_input('day_fourteen.txt')
    final_polymer = get_polymer_after_iterations(polymer, reactions_table, 10)
    print(get_answer(final_polymer))



if __name__ == '__main__':
    solve_day_one()
