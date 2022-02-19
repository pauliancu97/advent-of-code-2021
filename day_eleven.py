from matrix import Matrix
from utils import read_lines


OFFSETS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def get_matrix(path: str) -> Matrix[int]:
    lines = read_lines(path)
    digits = [[int(digit) for digit in line] for line in lines]
    return Matrix(digits)


def update_matrix(matrix: Matrix[int]) -> None:
    queue: list[tuple[int, int]] = []
    for row in range(0, matrix.rows):
        for col in range(0, matrix.cols):
            if matrix[row, col] == 9:
                matrix[row, col] = 0
                queue.append((row, col))
            else:
                matrix[row, col] += 1
    while len(queue) != 0:
        row, col = queue.pop(0)
        for row_offset, col_offset in OFFSETS:
            offseted_row = row + row_offset
            offseted_col = col + col_offset
            coordinates = (offseted_row, offseted_col)
            if matrix.has_coordinates(coordinates) and matrix[coordinates] != 0:
                if matrix[coordinates] == 9:
                    matrix[coordinates] = 0
                    queue.append(coordinates)
                else:
                    matrix[coordinates] += 1


def get_num_flashes(matrix: Matrix[int], steps: int) -> int:
    result = 0
    for _ in range(0, steps):
        update_matrix(matrix)
        for row in range(0, matrix.rows):
            for col in range(0, matrix.cols):
                if matrix[row, col] == 0:
                    result += 1
    return result


def get_synchronization_step(matrix: Matrix[int]) -> int:
    step = 0
    is_synchronized = False
    while not is_synchronized:
        step += 1
        update_matrix(matrix)
        num_flashes = 0
        for row in range(0, matrix.rows):
            for col in range(0, matrix.cols):
                if matrix[row, col] == 0:
                    num_flashes += 1
        is_synchronized = num_flashes == matrix.rows * matrix.cols
    return step


def solve_part_one() -> None:
    matrix = get_matrix('day_eleven.txt')
    print(get_num_flashes(matrix, 100))


def solve_part_two() -> None:
    matrix = get_matrix('day_eleven.txt')
    print(get_synchronization_step(matrix))


if __name__ == '__main__':
    solve_part_two()
