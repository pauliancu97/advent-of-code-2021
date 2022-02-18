from matrix import Matrix
from utils import read_lines


CELL_OFFSETS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_cave(path: str) -> Matrix[int]:
    lines = read_lines(path)
    list_matrix = [[int(digit) for digit in line] for line in lines]
    return Matrix[int](list_matrix)


def get_lowest_points(cave: Matrix[int]) -> list[int]:
    lowest_points: list[int] = []
    for row in range(0, cave.rows):
        for col in range(0, cave.cols):
            is_lowest_point = True
            for row_offset, col_offset in CELL_OFFSETS:
                offseted_row = row + row_offset
                offseted_col = col + col_offset
                if cave.has_coordinates((offseted_row, offseted_col)) and cave[offseted_row, offseted_col] <= cave[row, col]:
                    is_lowest_point = False
            if is_lowest_point:
                lowest_points.append(cave[row, col])
    return lowest_points


def get_lowest_points_coordinates(cave: Matrix[int]) -> list[tuple[int, int]]:
    lowest_points: list[tuple[int, int]] = []
    for row in range(0, cave.rows):
        for col in range(0, cave.cols):
            is_lowest_point = True
            for row_offset, col_offset in CELL_OFFSETS:
                offseted_row = row + row_offset
                offseted_col = col + col_offset
                if cave.has_coordinates((offseted_row, offseted_col)) and cave[offseted_row, offseted_col] <= cave[row, col]:
                    is_lowest_point = False
            if is_lowest_point:
                lowest_points.append((row, col))
    return lowest_points


def get_sum_risk_levels(cave: Matrix[int]) -> int:
    lowest_points = get_lowest_points(cave)
    return sum([point + 1 for point in lowest_points])


def get_basin_size(cave: Matrix[int], start: tuple[int, int]) -> int:
    visited = {start}
    queue = [start]
    while len(queue) != 0:
        row, col = queue[0]
        queue = queue[1:]
        for row_offset, col_offset in CELL_OFFSETS:
            offseted_row = row + row_offset
            offseted_col = col + col_offset
            coordinate = (offseted_row, offseted_col)
            if cave.has_coordinates(coordinate) and coordinate not in visited and cave[coordinate] != 9:
                queue.append(coordinate)
                visited.add(coordinate)
    return len(visited)


def get_part_two_answer(cave: Matrix[int]) -> int:
    lowest_points_coordinates = get_lowest_points_coordinates(cave)
    basin_sizes = [get_basin_size(cave, start) for start in lowest_points_coordinates]
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def solve_part_one() -> None:
    cave = get_cave('day_nine.txt')
    print(get_sum_risk_levels(cave))


def solve_part_two() -> None:
    cave = get_cave('day_nine.txt')
    print(get_part_two_answer(cave))


if __name__ == '__main__':
    solve_part_two()