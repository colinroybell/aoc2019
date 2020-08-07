import sys
import re


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0] * 3

    def str_array(self, name, arr):
        return "{}=<x={:3d}, y={:3d}, z={:3d}>". \
            format(name, arr[0], arr[1], arr[2])

    def __str__(self):
        return self.str_array("pos", self.pos) + ", " + \
            self.str_array("vel", self.vel)

    def update_vel(self, other):
        for i in range(0, 3):
            if self.pos[i] < other.pos[i]:
                self.vel[i] += 1
                other.vel[i] -= 1
            elif self.pos[i] > other.pos[i]:
                self.vel[i] -= 1
                other.vel[i] += 1

    def update_pos(self):
        for i in range(0, 3):
            self.pos[i] += self.vel[i]

    def energy(self):
        pot = 0
        kin = 0
        for i in range(0, 3):
            pot += abs(self.pos[i])
            kin += abs(self.vel[i])

        return pot * kin


def part_a(filename, steps, report_interval):

    xyz_re = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

    moons = []

    with open(filename, 'r') as f:
        for line in f:
            match = re.match(xyz_re, line)
            if match:
                moons.append(Moon([int(match.group(1)), int(match.group(2)),
                                   int(match.group(3))]))

    print("Initial")
    for moon in moons:
        print(moon)
    print("")

    for i in range(0, steps):
        for j in range(0, len(moons)):
            for k in range(j + 1, len(moons)):
                moons[j].update_vel(moons[k])

        for j in range(0, len(moons)):
            moons[j].update_pos()

        if (i % report_interval == 0):
            print("After {} steps".format(i))
            for moon in moons:
                print(moon)
            print("")

    energy = 0
    for moon in moons:
        energy += moon.energy()

    return energy


def part_b(filename):
    # The key to this is that x,y,z operate independently, so can look for
    # repeats in each axis independently
    xyz_re = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

    moons = []

    with open(filename, 'r') as f:
        for line in f:
            match = re.match(xyz_re, line)
            if match:
                moons.append(Moon([int(match.group(1)), int(match.group(2)),
                                   int(match.group(3))]))

    done = [0] * 3
    cache = [{}, {}, {}]
    diff = [0] * 3

    i = 0
    while sum(done) < 3:

        for d in range(0, 3):
            if done[d]:
                continue
            vec = []
            for moon in moons:
                vec.append(moon.pos[d])
                vec.append(moon.vel[d])
            tup = tuple(vec)
            if tup in cache[d]:
                # This is true in the three cases we have, so we don't
                # need to worry about the complexities of it not being
                assert(cache[d][tup] == 0)
                print("{}: {} repeats {}".format(d, i, cache[d][tup]))
                diff[d] = i - cache[d][tup]
                done[d] = 1
            else:
                cache[d][tup] = i

        for j in range(0, len(moons)):
            for k in range(j + 1, len(moons)):
                moons[j].update_vel(moons[k])

        for j in range(0, len(moons)):
            moons[j].update_pos()

        i += 1

    # In all cases we
    return lcm(diff[0], lcm(diff[1], diff[2]))


def day12a():
    return part_a('data/day12.txt', 1000, 100)


def day12b():
    return part_b('data/day12.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day12a())
    if 'b' in sys.argv:
        print(day12b())
