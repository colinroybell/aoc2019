from day18 import both_parts


def test_18a():
    assert(both_parts('data/day18_test1.txt', 'a') == 8)
    assert(both_parts('data/day18_test2.txt', 'a') == 86)
    assert(both_parts('data/day18_test3.txt', 'a') == 132)
    assert(both_parts('data/day18_test4.txt', 'a') == 136)
    assert(both_parts('data/day18_test5.txt', 'a') == 81)

def test_18b():
    assert(both_parts('data/day18_test6.txt', 'b') == 8)
    assert(both_parts('data/day18_test7.txt', 'b') == 24)
    assert(both_parts('data/day18_test8.txt', 'b') == 32)
    assert(both_parts('data/day18_test9.txt', 'b') == 72)
