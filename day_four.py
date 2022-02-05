from matrix import Matrix


def test():
    m = Matrix[int]([[0, 1, 2], [3, 4, 5]])
    print(m[0, 1])
    m[0, 1] = 6
    print(m[0, 1])
    print(2 in m)
    print(10 in m)
    print(m.rows)
    print(m.cols)


if __name__ == '__main__':
    test()