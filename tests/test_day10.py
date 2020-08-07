from day10 import part_a, part_b


def test_10a():
    assert(part_a('data/day10_test1.txt') == 8)
    assert(part_a('data/day10_test5.txt') == 210)

def test_10b():
    assert(part_b('data/day10_test5.txt') == 802)
