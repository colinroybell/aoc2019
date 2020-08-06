import sys
from functools import total_ordering


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def reduce_(v):
    g = gcd(abs(v[0]), abs(v[1]))
    return (v[0] / g, v[1] / g, g)


def neg(v):
    return (-v[0], -v[1])


def part_a(filename):
    loc = []
    vec = []
    with open(filename, 'r') as f:
        y = 0
        for line in f:
            for x in range(0, len(line)):
                if line[x] == '#':
                    loc.append((x, y))
                    vec.append(set())
            y += 1

    for i in range(0, len(loc)):
        for j in range(i + 1, len(loc)):
            v = (loc[j][0]-loc[i][0], loc[j][1]-loc[i][1])
            red_v = reduce_(v)[0:2]
            vec[i].add(red_v)
            vec[j].add(neg(red_v))

    max_ = 0
    for i in range(0, len(loc)):
        max_ = max(max_, len(vec[i]))

    return max_


@total_ordering
class Bucket:
    def __init__(self, v):
        self.x = v[0]
        self.y = v[1]
        self.nodes = []

    def append(self, node):
        self.nodes.append(node)

    def sort_nodes(self):
        self.nodes = sorted(self.nodes)

    def class_(self):
        if self.x > 0 or self.x == 0 and self.y < 0:
            return 0
        else:
            return 1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.class_() < other.class_():
            return True
        if self.class_() > other.class_():
            return False
        else:
            return self.x * other.y > self.y * other.x

    def __str__(self):
        string = "({} {} {}) ".format(self.x, self.y, self.class_())
        for node in self.nodes:
            string += node.__str__() + ' '

        return string


@total_ordering
class Node:
    def __init__(self, dist, ast):
        self.dist = dist
        self.ast = ast

    def __hash__(self):
        return self.dist

    def __eq__(self, other):
        return self.dist == other.dist

    def __lt__(self, other):
        return self.dist < other.dist

    def __str__(self):
        return "[{} {}]".format(self.dist, self.ast)


def part_b(filename):
    loc = []
    vec = []
    with open(filename, 'r') as f:
        y = 0
        for line in f:
            for x in range(0, len(line)):
                if line[x] == '#':
                    loc.append((x, y))
                    vec.append(set())
            y += 1

    for i in range(0, len(loc)):
        for j in range(i + 1, len(loc)):
            v = (loc[j][0] - loc[i][0], loc[j][1] - loc[i][1])
            red_v = reduce_(v)[0:2]
            vec[i].add(red_v)
            vec[j].add(neg(red_v))

    max_ = 0
    max_i = 0
    for i in range(0, len(loc)):
        if len(vec[i]) > max_:
            max_ = len(vec[i])
            max_i = i

    buckets = {}

    for j in range(0, len(loc)):
        if not j == max_i:
            v = (loc[j][0] - loc[max_i][0], loc[j][1] - loc[max_i][1])
            red_vg = reduce_(v)
            red_v = red_vg[0:2]
            dist = red_vg[2]

            val = loc[j][0] * 100 + loc[j][1]

            node = Node(dist, val)
            if red_v not in buckets:
                buckets[red_v] = Bucket(red_v)

            buckets[red_v].append(node)

    buckets_dict = buckets.items()

    buckets_sorted = sorted(buckets.items(), key=lambda x: x[1])

    for _, b in buckets_sorted:
        b.sort_nodes()

    vap = 0
    count = 200
    done = False
    last_vap = 0
    while not done:
        for _, b in buckets_sorted:
            if b.nodes:
                vap += 1
                node = b.nodes.pop(0)
                if vap == count:
                    done = True
                    last_vap = node.ast
                    break
    return last_vap


def day10a():
    return part_a('data/day10.txt')


def day10b():
    return part_b('data/day10.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day10a())
    if 'b' in sys.argv:
        print(day10b())
