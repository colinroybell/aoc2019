import sys
from intcode import State


def rotate_left(d):
    return(d[1], -d[0])


def rotate_right(d):
    return(-d[1], d[0])


def step(loc, d):
    return(loc[0] + d[0], loc[1] + d[1])


def both_parts(filename, part):
    f = open(filename, 'r')
    string = f.readline()
    f.close()

    input_pipe = []
    output_pipe = []

    loc = (0, 0)
    delta = (0, -1)
    squares = {}

    if part == 'b':
        squares[(0, 0)] = 1

    state = State(string, input_pipe=input_pipe, output_pipe=output_pipe)
    done = 0
    while not done:
        done = state.run_one_step()
        if state.waiting_for_input:
            if loc in squares:
                value = squares[loc]
            else:
                value = 0
            input_pipe.append(value)
        if len(output_pipe) >= 2:
            paint = output_pipe.pop(0)
            turn = output_pipe.pop(0)
            squares[loc] = paint
            if turn == 0:
                delta = rotate_left(delta)
            else:
                delta = rotate_right(delta)
            loc = step(loc, delta)

    if part == 'a':
        return len(squares)

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for loc in squares:
        min_x = min(min_x, loc[0])
        max_x = max(max_x, loc[0])
        min_y = min(min_y, loc[1])
        max_y = max(max_y, loc[1])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in squares:
                val = squares[(x, y)]
            else:
                val = 0
            if val:
                print('#', end='')
            else:
                print('.', end='')
        print('')

    return 0


def day11a():
    return both_parts('data/day11.txt', 'a')


def day11b():
    return both_parts('data/day11.txt', 'b')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day11a())
    if 'b' in sys.argv:
        print(day11b())
