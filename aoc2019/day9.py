import sys
from intcode import State


def both_parts(filename):
    f = open(filename, 'r')
    string = f.readline()
    f.close()

    state = State(string)
    return state.run()


def day9a_test1():
    f = open('data/day9_test1.txt', 'r')
    string = f.readline()
    f.close()

    state = State(string)
    ret = state.run()
    print(state)
    return ret

def day9a():
    return both_parts('data/day9.txt')


def day9b():
    return both_parts('data/day9.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day9a())
    if 'b' in sys.argv:
        print(day9b())
    if 'a_test1' in sys.argv:
        print(day9a_test1())
