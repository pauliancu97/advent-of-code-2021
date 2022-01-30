def read_lines(path: str) -> list[str]:
    with open(path) as file:
        return file.readlines()