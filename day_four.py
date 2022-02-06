from typing import Optional
from matrix import Matrix
from utils import read_lines


def get_bingo_numbers(line: str) -> list[int]:
    return [int(num_str) for num_str in line.split(',')]


def get_bingo_board(board_lines: list[str]) -> Matrix[int]:
    list_matrix = [[int(num_str) for num_str in line.split()] for line in board_lines]
    return Matrix[int](list_matrix)


def get_all_bingo_boards(lines: list[str]) -> list[Matrix[int]]:
    empty_lines_indices = [index for index, line in enumerate(lines) if len(line) == 0] + [len(lines)]
    boards_boundaries = zip(empty_lines_indices[:-1], empty_lines_indices[1:])
    return [get_bingo_board(lines[start + 1:end]) for start, end in boards_boundaries]


def get_processed_input(lines: list[str]) -> tuple[list[int], list[Matrix[int]]]:
    bingo_numbers = get_bingo_numbers(lines[0])
    bingo_boards = get_all_bingo_boards(lines[1:])
    return bingo_numbers, bingo_boards


def get_marked_bingo_board(drawn_bingo_numbers: list[int], bingo_board: Matrix[int]) -> Matrix[bool]:
    marked_bingo_board = Matrix[bool].with_default(bingo_board.rows, bingo_board.cols, False)
    for row in range(0, bingo_board.rows):
        for col in range(0, bingo_board.cols):
            if bingo_board[row, col] in drawn_bingo_numbers:
                marked_bingo_board[row, col] = True
    return marked_bingo_board


def is_winning_bingo_board(drawn_bingo_numbers: list[int], bingo_board: Matrix[int]) -> bool:
    marked_bingo_board = get_marked_bingo_board(drawn_bingo_numbers, bingo_board)
    for row in range(0, marked_bingo_board.rows):
        is_all_row_marked = True
        for col in range(0, marked_bingo_board.cols):
            if not marked_bingo_board[row, col]:
                is_all_row_marked = False
        if is_all_row_marked:
            return True
    for col in range(0, marked_bingo_board.cols):
        is_all_col_marked = True
        for row in range(0, marked_bingo_board.rows):
            if not marked_bingo_board[row, col]:
                is_all_col_marked = False
        if is_all_col_marked:
            return True
    return False


def get_first_winning_board(bingo_numbers: list[int], bingo_boards: list[Matrix[int]]) -> Optional[tuple[list[int], Matrix[int]]]:
    for end in range(1, len(bingo_numbers) + 1):
        for bingo_board in bingo_boards:
            if is_winning_bingo_board(bingo_numbers[:end], bingo_board):
                return bingo_numbers[:end], bingo_board
    return None


def get_last_winning_board(bingo_numbers: list[int], bingo_boards: list[Matrix[int]]) -> Optional[tuple[list[int], Matrix[int]]]:
    winning_boards_set = set[int]()
    for end in range(1, len(bingo_numbers) + 1):
        for index_bingo_board, bingo_board in enumerate(bingo_boards):
            if is_winning_bingo_board(bingo_numbers[:end], bingo_board):
                winning_boards_set.add(index_bingo_board)
                if len(winning_boards_set) == len(bingo_boards):
                    return bingo_numbers[:end], bingo_board
    return None


def get_bingo_score(drawn_bingo_numbers: list[int], bingo_board: Matrix[int]) -> int:
    marked_bingo_board = get_marked_bingo_board(drawn_bingo_numbers, bingo_board)
    unmarked_sum = 0
    for row in range(0, marked_bingo_board.rows):
        for col in range(0, marked_bingo_board.cols):
            if not marked_bingo_board[row, col]:
                unmarked_sum += bingo_board[row, col]
    return unmarked_sum * drawn_bingo_numbers[-1]


def solve_part_one() -> None:
    lines = read_lines('day_four.txt')
    bingo_numbers, bingo_boards = get_processed_input(lines)
    winning_result = get_first_winning_board(bingo_numbers, bingo_boards)
    if winning_result is not None:
        drawn_bingo_numbers, bingo_board = winning_result
        print(get_bingo_score(drawn_bingo_numbers, bingo_board))


def solve_part_two() -> None:
    lines = read_lines('day_four.txt')
    bingo_numbers, bingo_boards = get_processed_input(lines)
    winning_result = get_last_winning_board(bingo_numbers, bingo_boards)
    if winning_result is not None:
        drawn_bingo_numbers, bingo_board = winning_result
        print(get_bingo_score(drawn_bingo_numbers, bingo_board))


if __name__ == '__main__':
    solve_part_two()