import sys
from queue import PriorityQueue


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
                s = squares[(x, y)]
                print('{}'.format(s), end='')
            else:
                print('#', end='')
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

class Link:
    def __init__(self, node, length):
        self.node = node
        self.length = length


class Node:
    def __init__(self, loc, id):
        self.loc = loc
        self.id = id
        self.links = []

class State:
    def __init__(self, node, time, keys_got):
        self.node = node
        self.time = time
        self.keys_got = keys_got

    def __str__(self):
        return("{} {} {}".format(self.node.loc, self.time, self.keys_got))

    def __lt__(state,other):
        return False

    def __eq__(state,other):
        return True

def both_parts(filename, part):
    squares = {}
    keys = set()
    with open(filename, 'r') as f:
        y = 0
        for line in f:
            line = line.rstrip()
            for x in range(0, len(line)):
                c = line[x]
                squares[(x, y)] = c
                if c == '@':
                    start_loc = (x, y)
                if str.islower(c):
                    keys.add(c)
            y += 1
    output_grid(squares)
    print(keys)

    # Now collect nodes
    node = Node(start_loc,'@')
    start_node = node
    nodes = {}
    nodes_to_process = []
    nodes_to_process.append((node, 0))
    nodes[start_loc] = node
    #print("start node at {}".format(start_loc))

    while nodes_to_process:
        (node, node_input_dir) = nodes_to_process.pop()
        loc = node.loc
        #print("Processing from {} {}".format(loc, node_input_dir))
        for start_dir in range (1,5):
            loc = node.loc

            #print("Trying {}".format(start_dir))
            if start_dir == reverse(node_input_dir):
                #print("Rejecting {} backwards".format(start_dir))
                # Don't go back along the link we used to get here
                continue
            next_loc = forward(loc, start_dir)
            if squares[next_loc] == '#':
                #print("Rejecting {} nothing".format(start_dir))
                # Nothing this way
                continue



            dir = start_dir
            done = False
            dead_end = False
            length = 0
            input_dir = dir
            next_input_dir = 0
            loc = next_loc
            length = 1

            while not done:
                #print("at {}".format(loc))

                if squares[loc] != '.':
                    # Something interesting
                    done = True
                else:
                    exit_count = 0
                    for d in range(1,5):
                        if d == reverse(input_dir):
                            continue
                        test_loc = forward(loc, d)
                        if squares[test_loc] != '#':
                            exit_count += 1
                            next_loc = test_loc
                            next_input_dir = d

                    if exit_count == 0:
                        done = True
                        dead_end = True
                    if exit_count > 1:
                        # junction
                        done = True
                    if exit_count == 1:
                        input_dir = next_input_dir
                        loc = next_loc
                        length += 1

            if not dead_end:
                if loc in nodes:
                    new_node = nodes[loc]
                else:
                    #print("new node at {}".format(loc))
                    new_node = Node(loc, squares[loc])
                    nodes[loc] = new_node
                    nodes_to_process.append((new_node, input_dir))
                node.links.append(Link(new_node, length))
                new_node.links.append(Link(node, length))
            else:
                pass
                #print("dead end at {}".format(loc))

    opt_possible = 0
    for _,n in nodes.items():
        if len(n.links) == 2 and n.id == '.':
            print("Removing {}".format(n.loc))
            n0 = n.links[0].node
            n1 = n.links[1].node
            new_length = n.links[0].length + n.links[1].length
            for link in n0.links:
                if link.node == n:
                    link.node = n1
                    link.length = new_length
            for link in n1.links:
                if link.node == n:
                    link.node = n0
                    link.length = new_length

    queue = PriorityQueue()
    cache = {}

    queue.put((0, State(start_node, 0, set())))

    found = False
    best = 0

    while not found:
        queue_item = queue.get()

        state = queue_item[1]
        print(state)

        cache_key = (state.node.loc, frozenset(state.keys_got))

        if cache_key in cache:
            if cache[cache_key] < state.time:
                print("Already done in equal or better time")
        else:
            cache[cache_key] = state.time

        new_set = state.keys_got.copy()
        if str.islower(state.node.id):
            new_set.add(state.node.id)

        if new_set == keys:
            print("Found solution")
            found = True
            best = state.time

        for link in state.node.links:
            next_node = link.node
            if str.isupper(next_node.id) and str.lower(next_node.id) not in new_set:
                print("Can't go to {} as {} locked".format(next_node.loc, next_node.id))
            else:
                new_time = state.time + link.length
                cache_key = (next_node.loc, frozenset(new_set))
                if cache_key in cache and cache[cache_key] <= new_time:
                    # Already done better

                    pass
                else:
                    print("Pushing {} at time {} with {}".format(next_node.loc, new_time, new_set))
                    queue.put((new_time, State(next_node, new_time, new_set)))
                    cache[cache_key] = new_time

    return best



def day18a():
    return both_parts('data/day18.txt', 'a')


def day18b():
    return both_parts('data/day18.txt', 'b')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day18a())
    if 'b' in sys.argv:
        print(day18b())
