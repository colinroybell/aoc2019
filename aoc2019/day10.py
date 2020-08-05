import sys


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def reduce_(v):
    print(v)
    g = gcd(abs(v[0]), abs(v[1]))
    return (v[0] / g, v[1] / g)


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
                    print(x, y)
            y += 1

    for i in range(0, len(loc)):
        for j in range(i + 1, len(loc)):
            v = (loc[j][0]-loc[i][0], loc[j][1]-loc[i][1])
            print(i, j, v)
            red_v = reduce_(v)
            vec[i].add(red_v)
            vec[j].add(neg(red_v))

    max_ = 0
    for i in range(0, len(loc)):
        print("({} {}) {}".format(loc[i][0], loc[i][1], len(vec[i])))
        max_ = max(max_, len(vec[i]))

    return max_


def day10a():
    return part_a('data/day10.txt')


def day10b():
    return part_b('data/day10.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day10a())
    if 'b' in sys.argv:
        print(day10b())
