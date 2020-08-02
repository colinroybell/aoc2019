from day6 import State, part_a, part_b


def test_6a():
    assert(part_a('data/day6_test1.txt') == 42)
    assert(part_a('data/day6_test2.txt') == 6)


def test_6b():
    assert(part_b('data/day6_test3.txt') == 4)
