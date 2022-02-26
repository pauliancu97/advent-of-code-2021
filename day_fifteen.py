from copy import deepcopy
from matrix import Matrix
from utils import read_lines
from heapq import heappop, heappush


Coordinate = tuple[int, int]


def get_costs(path: str) -> Matrix[int]:
    lines = read_lines(path)
    values = [[int(digit) for digit in line] for line in lines]
    return Matrix(values)


def get_distance(costs: Matrix[int], source: Coordinate, destination: Coordinate) -> int:
    distances: Matrix[float] = Matrix.with_default(costs.rows, costs.cols, float('inf'))
    unvisited: set[Coordinate] = {(row, col) for row in range(0, costs.rows) for col in range(0, costs.cols)}
    distances[source] = 0.0
    queue = [(0.0, source)]
    while len(queue) != 0:
        distance, current_coordinate = heappop(queue)
        unvisited.remove(current_coordinate)
        for neighbour in costs.get_neighbours(current_coordinate):
            if neighbour in unvisited:
                if distance + costs[neighbour] < distances[neighbour]:
                    distances[neighbour] = distance + costs[neighbour]
                    heappush(queue, (distances[neighbour], neighbour))
    return int(distances[destination])


def get_incremented_matrix(matrix: Matrix[int]) -> Matrix[int]:
    result = Matrix[int].with_default(matrix.rows, matrix.cols, 0)
    for row in range(0, matrix.rows):
        for col in range(0, matrix.cols):
            if matrix[row, col] == 9:
                result[row, col] = 1
            else:
                result[row, col] = matrix[row, col] + 1
    return result


def get_incremented_matrices(original_matrix: Matrix[int], rows: int, cols: int) -> Matrix[Matrix[int]]:
    matrices = Matrix[Matrix[int]].with_default(rows, cols, Matrix[int].with_default(original_matrix.rows, original_matrix.cols, 0))
    for row in range(0, matrices.rows):
        for col in range(0, matrices.cols):
            if row == 0 and col == 0:
                matrices[row, col] = deepcopy(original_matrix)
            elif col == 0:
                matrices[row, col] = get_incremented_matrix(matrices[row - 1, col])
            else:
                matrices[row, col] = get_incremented_matrix(matrices[row, col - 1])
    return matrices


def place(source: Matrix[int], coordinates: Coordinate, destination: Matrix[int]) -> None:
    start_row, start_col = coordinates
    for row in range(0, source.rows):
        for col in range(0, source.cols):
            destination[start_row + row, start_col + col] = source[row, col]


def get_expanded_matrix(original_matrix: Matrix[int], rows: int, cols: int) -> Matrix[int]:
    incremented_matrices = get_incremented_matrices(original_matrix, rows, cols)
    expanded_rows = rows * original_matrix.rows
    expanded_cols = cols * original_matrix.cols
    expanded_matrix = Matrix[int].with_default(expanded_rows, expanded_cols, 0)
    for row in range(rows):
        for col in range(cols):
            start_coordinate = (row * original_matrix.rows, col * original_matrix.cols)
            place(incremented_matrices[row, col], start_coordinate, expanded_matrix)
    return expanded_matrix


def solve_part_one() -> None:
    costs = get_costs('day_fifteen.txt')
    source = (0, 0)
    destination = (costs.rows - 1, costs.cols - 1)
    distance = get_distance(costs, source, destination)
    print(distance)


def solve_part_two() -> None:
    costs = get_costs('day_fifteen.txt')
    expanded_costs = get_expanded_matrix(costs, 5, 5)
    source = (0, 0)
    destination = (expanded_costs.rows - 1, expanded_costs.cols - 1)
    distance = get_distance(expanded_costs, source, destination)
    print(distance)


if __name__ == '__main__':
    solve_part_two()