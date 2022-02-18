from utils import read_lines


def get_sum(n: int) -> int:
    return (n * (n + 1)) // 2

def get_cost_of_least_expensive_position(positions: list[int]) -> int:
    max_position = max(positions)
    min_position = min(positions)
    min_cost = 0
    for index, current_position in enumerate(range(min_position, max_position + 1)):
        cost = sum([abs(current_position - position) for position in positions])
        if index == 0:
            min_cost = cost
        elif min_cost > cost:
            min_cost = cost
    return min_cost


def get_cost_of_least_expensive_position_part_two(positions: list[int]) -> int:
    max_position = max(positions)
    min_position = min(positions)
    min_cost = 0
    for index, current_position in enumerate(range(min_position, max_position + 1)):
        cost = sum([get_sum(abs(current_position - position)) for position in positions])
        if index == 0:
            min_cost = cost
        elif min_cost > cost:
            min_cost = cost
    return min_cost

def get_positions(path: str) -> list[int]:
    line = read_lines(path)[0]
    return [int(string) for string in line.split(',')]


def solve_part_one() -> None:
    positions = get_positions('day_seven.txt')
    print(get_cost_of_least_expensive_position(positions))


def solve_part_two() -> None:
    positions = get_positions('day_seven.txt')
    print(get_cost_of_least_expensive_position_part_two(positions))


if __name__ == '__main__':
    solve_part_two()
