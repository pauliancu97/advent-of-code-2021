from re import compile as regex_compile
from typing import Optional
from utils import read_lines


EDGE_REGEX = regex_compile(r'(\w+)-(\w+)')


def get_edge(line: str) -> Optional[tuple[str, str]]:
    match = EDGE_REGEX.match(line)
    if match:
        return match.group(1, 2)
    return None


def get_edges(lines: list[str]) -> list[tuple[str, str]]:
    return [opt_edge for opt_edge in [get_edge(line) for line in lines] if opt_edge]


def get_graph(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for first_node, second_node in edges:
        if first_node in graph:
            graph[first_node] += [second_node]
        else:
            graph[first_node] = [second_node]
        if second_node in graph:
            graph[second_node] += [first_node]
        else:
            graph[second_node] = [first_node]
    return graph


def read_graph(path: str) -> dict[str, list[str]]:
    lines = read_lines(path)
    edges = get_edges(lines)
    return get_graph(edges)


def search_path_helper(graph: dict[str, list[str]], current_path: list[str], paths: list[list[str]]) -> None:
    node = current_path[-1]
    if node == 'end':
        if current_path not in paths:
            paths.append(current_path)
        return
    for neighbour in graph[node]:
        if neighbour.isupper() or neighbour not in current_path:
            search_path_helper(graph, current_path + [neighbour], paths)


def search_path_special_node_helper(graph: dict[str, list[str]], current_path: list[str], special_node: str, paths: list[list[str]]) -> None:
    node = current_path[-1]
    if node == 'end':
        if current_path not in paths:
            paths.append(current_path)
        return
    for neighbour in graph[node]:
        if neighbour.isupper() or ((neighbour not in current_path) or (neighbour == special_node and current_path.count(neighbour) <= 1)):
            search_path_special_node_helper(graph, current_path + [neighbour], special_node, paths)


def get_paths(graph: dict[str, list[str]]) -> list[list[str]]:
    paths: list[list[str]] = []
    search_path_helper(graph, ['start'], paths)
    return paths


def get_paths_with_special_node(graph: dict[str, list[str]]) -> list[list[str]]:
    paths: list[list[str]] = []
    lower_case_nodes = [node for node in graph.keys() if node.islower() and node != 'start' and node != 'end']
    for special_node in lower_case_nodes:
        search_path_special_node_helper(graph, ['start'], special_node, paths)
    return paths


def solve_part_one() -> None:
    graph = read_graph('day_twelve.txt')
    num_paths = len(get_paths(graph))
    print(num_paths)


def solve_part_two() -> None:
    graph = read_graph('day_twelve.txt')
    num_paths = len(get_paths_with_special_node(graph))
    print(num_paths)


if __name__ == '__main__':
    solve_part_two()