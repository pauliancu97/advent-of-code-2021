from copy import deepcopy
from utils import read_lines
from matrix import Matrix


NORMAL_CYCLE_TIMER_VALUE = 6
FIRST_CYCLE_TIMER_VALUE = 8
NUM_ITER = 80
NUM_ITER_PART_TWO = 256


def get_next_timers(timers: list[int]) -> list[int]:
    updated_timers = deepcopy(timers)
    for index, timer in enumerate(timers):
        if timer == 0:
            updated_timers[index] = NORMAL_CYCLE_TIMER_VALUE
            updated_timers.append(FIRST_CYCLE_TIMER_VALUE)
        else:
            updated_timers[index] = timer - 1
    return updated_timers


def get_timers_after_iterations(timers: list[int], num_iterations: int) -> list[int]:
    for _ in range(0, num_iterations):
        timers = get_next_timers(timers)
    return timers

def get_timers(path: str) -> list[int]:
    line = read_lines(path)[0]
    return [int(string) for string in line.split(',')]


def get_num_timers(timers: list[int], end_time: int) -> int:
    matrix = Matrix[int].with_default(end_time + 1, FIRST_CYCLE_TIMER_VALUE + 1, 0)
    for start_time in reversed(range(0, end_time + 1)):
        for timer_value in range(0, FIRST_CYCLE_TIMER_VALUE + 1):
            next_start_time = start_time + timer_value + 1
            if next_start_time > end_time:
                matrix[start_time, timer_value] = 0
            else:
                num_spawned_timers = 1 + (end_time - next_start_time) // (NORMAL_CYCLE_TIMER_VALUE + 1)
                matrix[start_time, timer_value] = num_spawned_timers
                spawned_timers = [(next_start_time + index * (NORMAL_CYCLE_TIMER_VALUE + 1), FIRST_CYCLE_TIMER_VALUE) for index in range(0, num_spawned_timers)]
                for spawned_start_time, spawned_timer_value in spawned_timers:
                    if spawned_start_time <= end_time:
                        matrix[start_time, timer_value] += matrix[spawned_start_time, spawned_timer_value]
    result = len(timers)
    for timer_value in timers:
        result += matrix[0, timer_value]
    return result


def solve_part_one() -> None:
    timers = get_timers('day_six.txt')
    final_timers = get_timers_after_iterations(timers, NUM_ITER)
    print(len(final_timers))


def solve_part_two() -> None:
    timers = get_timers('day_six.txt')
    num_timers = get_num_timers(timers, 256)
    print(num_timers)


if __name__ == '__main__':
    solve_part_two()

