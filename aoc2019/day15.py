import random
import sys
from intcode import State

# 0 is open
# 1 is wall
# 2 is unknown
# For part B, set to -dist from oxygen


def output_grid(squares):
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
                s = ['.', '#', '?'][val]
                if x == 0 and y == 0:
                    s = '*'
                print('{}'.format(s), end='')
            else:
                print('.', end='')
        print('')


def turn_left(dir):
    return [0, 3, 2, 4, 1][dir]


def turn_right(dir):
    return [0, 4, 2, 3, 1][dir]


def reverse(dir):
    return [0, 2, 1, 4, 3][dir]


def forward(loc, dir):
    (x, y) = loc
    if dir == 1:
        return (x, y-1)
    if dir == 2:
        return (x, y+1)
    if dir == 3:
        return (x-1, y)
    if dir == 4:
        return (x+1, y)
    assert(0)


class SearchNode:
    def __init__(self, loc, instructions):
        self.loc = loc
        self.instructions = instructions

    def get_instructions(self):
        return self.instructions

    def get_reverse_instructions(self):
        ret = []
        for r in reversed(self.instructions):
            ret.append(reverse(r))
        return ret

    def __repr__(self):
        return "{}".format(self.loc)


def discover_square(squares, search_nodes, loc, base_instructions):
    squares[loc] = 0
    for d in range(1, 5):
        new_loc = forward(loc, d)
        if new_loc not in squares:
            squares[new_loc] = 2
            search_nodes.append(SearchNode(new_loc, base_instructions + [d]))


def discover_square_part_b(squares, search_nodes, loc, base_instructions):
    print("Starting from {}".format(loc))
    for d in range(1, 5):
        new_loc = forward(loc, d)
        if new_loc in squares and squares[new_loc] == 0:
            squares[new_loc] = squares[loc] - 1  # one further away
            print(new_loc, squares[new_loc])
            search_nodes.append(SearchNode(new_loc, base_instructions + [d]))


def both_parts(filename, part):
    # Implemented a very naive (and inefficient) breadth-first search where
    # we go back to the original square all the time. Easy to code, but various
    # improvements possible
    f = open(filename, 'r')
    string = f.readline()
    f.close()

    input_pipe = []
    output_pipe = []

    state = State(string, input_pipe=input_pipe, output_pipe=output_pipe)

    squares = {}

    loc = (0, 0)
    squares[loc] = ()
    search_nodes = []

    forward_instructions = []
    return_instructions = []
    depth = 0
    oxygen_loc = (0, 0)

    done = False
    while not done:
        done = state.run_one_step()
        if state.waiting_for_input:
            if output_pipe and output_pipe[-1] == 2:
                # Done
                if part == 'a':
                    return depth
                else:
                    oxygen_loc = loc
                    discover_square(squares, search_nodes, loc,
                                    forward_instructions)
                    input_pipe.extend(return_instructions)
            elif loc == (0, 0) or output_pipe[-1] == 1:
                # Either start or we've found the new square
                discover_square(squares, search_nodes, loc,
                                forward_instructions)
                input_pipe.extend(return_instructions)
            else:
                print("{} is a wall".format(loc))
                # New square is a wall
                squares[loc] = 1
                input_pipe.extend(return_instructions[1:])
            while (output_pipe):
                output_pipe.pop()
            if search_nodes:
                node = search_nodes.pop(0)
                forward_instructions = node.instructions
                depth = len(forward_instructions)
                input_pipe.extend(node.instructions)
                loc = node.loc
                return_instructions = node.get_reverse_instructions()
            else:
                done = True

    done = False
    loc = oxygen_loc
    squares[loc] = -1
    discover_square_part_b(squares, search_nodes, loc, [])
    min_ = 0
    while not done:
        print("looping with {}".format(loc))
        if not search_nodes and not loc == oxygen_loc:
            done = True
        else:
            node = search_nodes.pop(0)
            loc = node.loc
            min_ = min(min_, squares[loc])
            discover_square_part_b(squares, search_nodes, loc, [])

    return -min_ - 1


def day15a():
    return both_parts('data/day15.txt', 'a')


def day15b():
    return both_parts('data/day15.txt', 'b')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day15a())
    if 'b' in sys.argv:
        print(day15b())
