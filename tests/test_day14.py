from day14 import both_parts


def test_14a():
    assert(both_parts('data/day14_test1.txt', 'a') == 31)
    assert(both_parts('data/day14_test2.txt', 'a') == 165)
    assert(both_parts('data/day14_test3.txt', 'a') == 13312)
    assert(both_parts('data/day14_test4.txt', 'a') == 180697)
    assert(both_parts('data/day14_test5.txt', 'a') == 2210736)


def test_14b():
    assert(both_parts('data/day14_test3.txt', 'b') == 82892753)
    assert(both_parts('data/day14_test4.txt', 'b') == 5586022)
    assert(both_parts('data/day14_test5.txt', 'b') == 460664)
