def read_lines(path: str) -> list[str]:
    with open(path) as file:
        return [line.replace('\n', '') for line in file.readlines()]