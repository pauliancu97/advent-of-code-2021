from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from math import ceil, floor
from typing import Optional
from utils import read_lines


@dataclass
class Number:
    value: int
    parent: Optional[Pair] = None

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Pair:
    first: Element
    second: Element
    parent: Optional[Pair] = None

    def __repr__(self) -> str:
        return f'[{self.first},{self.second}]'

    def __str__(self) -> str:
        return self.__repr__()


Element = Number | Pair


def get_parsed_element(string: str) -> tuple[Element, str]:
    if string[0].isdigit():
        index = 0
        while index < len(string) and string[index].isdigit():
            index += 1
        number = int(string[:index])
        return Number(number), string[index:]
    else:
        string = string[1:]
        first, remaining_string = get_parsed_element(string)
        string = remaining_string[1:]
        second, remaining_string = get_parsed_element(string)
        return Pair(first, second), remaining_string[1:]


def get_element_helper(node: Element, parent: Optional[Pair]) -> None:
    node.parent = parent
    if isinstance(node, Pair):
        get_element_helper(node.first, node)
        get_element_helper(node.second, node)


def get_element(string: str) -> Element:
    element, _ = get_parsed_element(string)
    get_element_helper(element, None)
    return element


def should_explode_helper(node: Element, depth: int) -> bool:
    match node:
        case Number(_, _):
            return False
        case Pair(Number(_, _), Number(_, _), _) if depth >= 4:
            return True
        case Pair(first, second, _):
            if should_explode_helper(first, depth + 1):
                return True
            if should_explode_helper(second, depth + 1):
                return True
            return False


def should_explode(node: Element) -> bool:
    return should_explode_helper(node, 0)


def should_split(node: Element) -> bool:
    match node:
        case Number(value, _) if value >= 10:
            return True
        case Pair(first, second, _):
            if should_split(first):
                return True
            if should_split(second):
                return True
            return False
        case _:
            return False


def add_first_value(pair: Pair, value: int) -> None:
    while pair.parent is not None and pair is pair.parent.first:
        pair = pair.parent
    if pair.parent is None:
        return
    node: Element = pair.parent.first
    while not isinstance(node, Number):
        node = node.second
    node.value += value


def add_second_value(pair: Pair, value: int) -> None:
    while pair.parent is not None and pair is pair.parent.second:
        pair = pair.parent
    if pair.parent is None:
        return
    node: Element = pair.parent.second
    while not isinstance(node, Number):
        node = node.first
    node.value += value


def get_exploded_helper(node: Element, depth: int) -> tuple[Element, bool]:
    match node:
        case Pair(Number(first_value, _), Number(second_value, _), parent) if depth >= 4:
            add_first_value(node, first_value)
            add_second_value(node, second_value)
            return Number(0, parent), True
        case Number(_, _):
            return node, False
        case Pair(first, second, parent):
            first_exploded, has_exploded_first = get_exploded_helper(first, depth + 1)
            if has_exploded_first:
                node.first = first_exploded
                return node, True
            second_exploded, has_exploded_second = get_exploded_helper(second, depth + 1)
            if has_exploded_second:
                node.second = second_exploded
                return node, True
            return node, False


def get_splitted_helper(node: Element) -> tuple[Element, bool]:
    match node:
        case Number(value, parent) if value >= 10:
            new_node = Pair(Number(floor(value / 2)), Number(ceil(value / 2)), parent)
            new_node.first.parent = new_node
            new_node.second.parent = new_node
            return new_node, True
        case Pair(first, second, parent):
            splitted_first, has_splitted_first = get_splitted_helper(first)
            if has_splitted_first:
                node.first = splitted_first
                return node, True
            splitted_second, has_splitted_second = get_splitted_helper(second)
            if has_splitted_second:
                node.second = splitted_second
                return node, True
            return node, False
        case _:
            return node, False


def get_exploded(node: Element) -> Element:
    return get_exploded_helper(node, 0)[0]


def get_splitted(node: Element) -> Element:
    return get_splitted_helper(node)[0]


def get_reduced(node: Element) -> Element:
    while True:
        if should_explode(node):
            node = get_exploded(node)
        elif should_split(node):
            node = get_splitted(node)
        else:
            break
    return node


def get_added(first: Element, second: Element) -> Element:
    temp = Pair(first, second)
    first.parent = temp
    second.parent = temp
    return get_reduced(temp)


def get_magnitude(element: Element) -> int:
    match element:
        case Number(value, _):
            return value
        case Pair(first, second, _):
            first_magnitude = get_magnitude(first)
            second_magnitude = get_magnitude(second)
            return 3 * first_magnitude + 2 * second_magnitude


def solve_part_one() -> None:
    lines = read_lines('day_eightteen.txt')
    elements = [get_element(line) for line in lines]
    result_element = reduce(lambda acc, x: get_added(acc, x), elements)
    print(get_magnitude(result_element))


if __name__ == '__main__':
    solve_part_one()