from __future__ import annotations
from enum import Enum
from utils import read_lines
from matrix import Matrix
from typing import Callable, Optional
from dataclasses import dataclass
from heapdict import heapdict


class Tile(Enum):
    EMPTY = ' '
    FREE = '.'
    WALL = '#'
    AMBER = 'A'
    BRONZE = 'B'
    COPPER = 'C'
    DESERT = 'D'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def to_amphipod(self: Tile) -> Optional[AmphipodType]:
        match self:
            case Tile.AMBER | Tile.BRONZE | Tile.COPPER | Tile.DESERT:
                return AmphipodType(self.value)
            case _:
                return None

    def is_free(self) -> bool:
        return self == Tile.FREE


class AmphipodType(Enum):
    AMBER = 'A'
    BRONZE = 'B'
    COPPER = 'C'
    DESERT = 'D'

    def get_destination_col(self) -> int:
        match self:
            case AmphipodType.AMBER:
                return 3
            case AmphipodType.BRONZE:
                return 5
            case AmphipodType.COPPER:
                return 7
            case AmphipodType.DESERT:
                return 9

    def to_tile(self) -> Tile:
        match self:
            case AmphipodType.AMBER:
                return Tile.AMBER
            case AmphipodType.BRONZE:
                return Tile.BRONZE
            case AmphipodType.COPPER:
                return Tile.COPPER
            case AmphipodType.DESERT:
                return Tile.DESERT


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int


@dataclass(frozen=True)
class Amphipod:
    type: AmphipodType
    coordinate: Coordinate

    def is_in_side_room(self) -> bool:
        return self.coordinate.row >= 2

    def get_cost(self, distance: int) -> int:
        match self.type:
            case AmphipodType.AMBER:
                return distance
            case AmphipodType.BRONZE:
                return distance * 10
            case AmphipodType.COPPER:
                return distance * 100
            case AmphipodType.DESERT:
                return distance * 1000

    def get_destination_col(self) -> int:
        match self.type:
            case AmphipodType.AMBER:
                return 3
            case AmphipodType.BRONZE:
                return 5
            case AmphipodType.COPPER:
                return 7
            case AmphipodType.DESERT:
                return 9


Map = Matrix[Tile]
ImmutableMap = tuple[tuple[Tile, ...], ...]
State = tuple[ImmutableMap, int]


def get_immutable_map(map: Map) -> ImmutableMap:
    return tuple([tuple([map[row, col] for col in range(map.cols)]) for row in range(map.rows)])


def get_mutable_map(map: ImmutableMap) -> Map:
    rows = len(map)
    cols = len(map[0])
    tiles = [[map[row][col] for col in range(cols)] for row in range(rows)]
    return Matrix(tiles)


def get_input(path: str) -> Map:
    lines = read_lines(path)
    tiles = [[Tile(character) for character in line] for line in lines]
    return Matrix(tiles)


def get_amphipods(map: Map) -> list[Amphipod]:
    opt_amphipods = [(map[row, col].to_amphipod(), (row, col)) for row in range(map.rows) for col in range(map.cols)]
    return [Amphipod(opt_amp, Coordinate(coord[0], coord[1])) for opt_amp, coord in opt_amphipods if opt_amp]


def is_at_destination(amphipod: Amphipod, map: Map) -> bool:
    destination_col = amphipod.get_destination_col()
    if destination_col == amphipod.coordinate.col:
        return amphipod.coordinate.row == 3 or (amphipod.coordinate.row == 2 and map[3, destination_col].to_amphipod() == amphipod.type)
    else:
        return False


def get_reachable_destination_row(amphipod: Amphipod, map: Map) -> Optional[int]:
    destination_col = amphipod.get_destination_col()
    if map[3, destination_col].is_free():
        return 3
    elif map[2, destination_col].is_free() and map[3, destination_col].to_amphipod() == amphipod.type:
        return 2
    else:
        return None


def is_col_reachable(map: Map, start: int, end: int) -> bool:
    result = True
    begin = min(start, end) + (1 if start < end else 0)
    finish = max(start, end) - (1 if start > end else 0)
    for col in range(begin, finish + 1):
        if not map[1, col].is_free():
            result = False
    return result


def get_actions(amphipod: Amphipod, map: Map) -> list[tuple[Coordinate, int]]:
    actions: list[tuple[Coordinate, int]] = []
    if not is_at_destination(amphipod, map):
        if amphipod.is_in_side_room():
            if map[amphipod.coordinate.row -1, amphipod.coordinate.col].is_free():
                offset_distance = 1 if amphipod.coordinate.row == 2 else 2
                destination_col = amphipod.get_destination_col()
                destination_row = get_reachable_destination_row(amphipod, map)
                if destination_row:
                    if is_col_reachable(map, amphipod.coordinate.col, destination_col):
                        offset_distance += (1 if  destination_row == 2 else 2)
                        distance = abs(amphipod.coordinate.col - destination_col) + offset_distance
                        actions.append((Coordinate(destination_row, destination_col), amphipod.get_cost(distance)))
                        return actions
                possible_cols = [1, 2, 4, 6, 8, 10, 11]
                for possible_col in possible_cols:
                    if is_col_reachable(map, amphipod.coordinate.col, possible_col):
                        distance = abs(amphipod.coordinate.col - possible_col) + offset_distance
                        actions.append((Coordinate(1, possible_col), amphipod.get_cost(distance)))
                return actions
        else:
            destination_col = amphipod.get_destination_col()
            is_destination_free = map[3, destination_col].is_free() or (map[3, destination_col].to_amphipod() == amphipod.type and map[2, destination_col].is_free())
            if is_destination_free:
                distance_offset = 2 if map[3, destination_col].is_free() else 1
                destination_row = 3 if map[3, destination_col].is_free() else 2
                if is_col_reachable(map, amphipod.coordinate.col, destination_col):
                    distance = abs(amphipod.coordinate.col - destination_col) + distance_offset
                    actions.append((Coordinate(destination_row, destination_col), amphipod.get_cost(distance)))
            return actions
    return actions


def get_neighbours(map: ImmutableMap) -> list[tuple[ImmutableMap, int]]:
    neighbours: list[tuple[ImmutableMap, int]] = []
    mutable_map = get_mutable_map(map)
    amphipods = get_amphipods(mutable_map)
    for amphipod in amphipods:
        actions = get_actions(amphipod, mutable_map)
        for coordinate, cost in actions:
            mutable_map[amphipod.coordinate.row, amphipod.coordinate.col] = Tile.FREE
            mutable_map[coordinate.row, coordinate.col] = amphipod.type.to_tile()
            neighbour = get_immutable_map(mutable_map)
            neighbours.append((neighbour, cost))
            mutable_map[amphipod.coordinate.row, amphipod.coordinate.col] = amphipod.type.to_tile()
            mutable_map[coordinate.row, coordinate.col] = Tile.FREE
    return neighbours


def get_a_star_result(start: ImmutableMap, heuristic: Callable[[ImmutableMap], int]) -> int:
    g: dict[ImmutableMap, int] = {}
    g[start] = 0
    f: dict[ImmutableMap, int] = {}
    f[start] = heuristic(start)
    open_set = heapdict()
    open_set[start] = f[start]
    while len(open_set) != 0:
        item = open_set.popitem()
        current: ImmutableMap = item[0]
        cost: int = item[1]
        if is_immutable_map_goal(current):
            return cost
        for neighbour, neighbour_cost in get_neighbours(current):
            new_cost = g[current] + neighbour_cost
            if neighbour not in g or new_cost < g[neighbour]:
                g[neighbour] = new_cost
                f[neighbour] = new_cost + heuristic(neighbour)
                open_set[neighbour] = f[neighbour]
    return 0


def get_heuristic_cost(map: ImmutableMap) -> int:
    mutable_map = get_mutable_map(map)
    amphipods = get_amphipods(mutable_map)
    cost = 0
    for amphipod in amphipods:
        if not (amphipod.is_in_side_room() and amphipod.coordinate.col == amphipod.get_destination_col()):
            distance = 0
            distance += amphipod.coordinate.row - 1
            distance += abs(amphipod.coordinate.col - amphipod.get_destination_col())
            distance += 1
            cost += amphipod.get_cost(distance)
    return cost


def is_goal(map: Map) -> bool:
    result = True
    for amphipod_type in AmphipodType:
        col = amphipod_type.get_destination_col()
        for row in range(2, 4):
            if map[row, col].to_amphipod() != amphipod_type:
                result = False
    return result


def is_immutable_map_goal(map: ImmutableMap) -> bool:
    result = True
    for amphipod_type in AmphipodType:
        col = amphipod_type.get_destination_col()
        for row in range(2, 4):
            if map[row][col].to_amphipod() != amphipod_type:
                result = False
    return result


def search_solution_helper(map: Map, current_cost: int, current_states: set[State], result: list[Optional[int]]) -> None:
    immutable_map = get_immutable_map(map)
    if (immutable_map, current_cost) in current_states:
        return
    current_states.add((immutable_map, current_cost))
    if is_goal(map):
        current_best_result = result[0]
        if current_best_result is None or current_cost < current_best_result:
            result[0] = current_cost
    else:
        amphipods = get_amphipods(map)
        for amphipod in amphipods:
            actions = get_actions(amphipod, map)
            for action in actions:
                destination , cost = action
                map[destination.row, destination.col] = amphipod.type.to_tile()
                map[amphipod.coordinate.row, amphipod.coordinate.col] = Tile.FREE
                search_solution_helper(map, current_cost + cost, current_states, result)
                map[destination.row, destination.col] = Tile.FREE
                map[amphipod.coordinate.row, amphipod.coordinate.col] = amphipod.type.to_tile()


#def search_solution(map: Map) -> int:
#    result_container: list[Optional[int]] = [None]
#    states: set[State] = set()
#    search_solution_helper(map, 0, states, result_container)
#    result = result_container[0]
#    return 0 if result is None else result


def search_solution(map: Map) -> int:
    return get_a_star_result(get_immutable_map(map), get_heuristic_cost)


def solve_part_one() -> None:
    map = get_input('day_twentythree.txt')
    print(search_solution(map))


if __name__ == '__main__':
    solve_part_one()