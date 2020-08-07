from day12 import part_a, part_b


def test_12a():
    assert(part_a('data/day12_test1.txt', 10, 1) == 179)
    assert(part_a('data/day12_test2.txt', 100, 10) == 1940)


def test_10b():
    assert(part_b('data/day12_test1.txt') == 2772)
    assert(part_b('data/day12_test2.txt') == 4686774924)
