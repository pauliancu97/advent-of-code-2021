from utils import read_lines


def get_depths(lines: list[str]) -> list[int]:
    return [int(line) for line in lines]


def get_three_sliding_windows(depths: list[int]) -> list[int]:
    return [depths[index] + depths[index + 1] + depths[index + 2] for index in range(0, len(depths) - 2)]


def get_answer(depths: list[int]) -> int:
    return len([current for previous, current in zip(depths[:-1], depths[1:]) if previous < current])


def solve_part_one() -> None:
    lines = read_lines("day_one.txt")
    depths = get_depths(lines)
    print(get_answer(depths))


def solve_parth_two() -> None:
    lines = read_lines("day_one.txt")
    depths = get_depths(lines)
    three_sliding_windows = get_three_sliding_windows(depths)
    print(get_answer(three_sliding_windows))


if __name__ == '__main__':
    solve_parth_two()