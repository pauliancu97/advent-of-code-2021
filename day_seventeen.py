from dataclasses import dataclass
from vector import Vector
from re import compile as regex_compile
from utils import read_lines


@dataclass(frozen=True)
class Target:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def __contains__(self, position: Vector) -> bool:
        return position.x in range(self.x_min, self.x_max + 1) and position.y in range(self.y_min, self.y_max + 1)


def get_gaussian_sum(n: int) -> int:
    return n * (n + 1) // 2


def get_target(string: str) -> Target:
    regex = regex_compile(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')
    match = regex.match(string)
    if match:
        x_min, x_max, y_min, y_max = (int(num) for num in match.group(1, 2, 3, 4))
        return Target(x_min, x_max, y_min, y_max)
    raise ValueError

def get_min_x_speed(x_min: int) -> int:
    result = 0
    while get_gaussian_sum(result) < x_min:
        result += 1
    return result


def get_min_speeds(target: Target) -> tuple[int, int, int, int]:
    x_speed_min = get_min_x_speed(target.x_min)
    x_speed_max = target.x_max
    y_speed_min = target.y_min
    y_speed_max = abs(target.y_min) - 1
    return x_speed_min, x_speed_max, y_speed_min, y_speed_max

def trajectory_intersects_target(velocity: Vector, target: Target) -> bool:
    position = Vector(0, 0)
    while position.y >= target.y_min:
        if position in target:
            return True
        position = position + velocity
        velocity = Vector(x=0 if velocity.x == 0 else velocity.x - 1, y=velocity.y - 1)
    return False


def get_num_trajectories_hitting_target(target: Target) -> int:
    result = 0
    x_speed_min, x_speed_max, y_speed_min, y_speed_max = get_min_speeds(target)
    for x_speed in range(x_speed_min, x_speed_max + 1):
        for y_speed in range(y_speed_min, y_speed_max + 1):
            if trajectory_intersects_target(Vector(x_speed, y_speed), target):
                result += 1
    return result


def solve_part_one() -> None:
    line = read_lines('day_seventeen.txt')[0]
    target = get_target(line)
    print(get_num_trajectories_hitting_target(target))


if __name__ == '__main__':
    solve_part_one()