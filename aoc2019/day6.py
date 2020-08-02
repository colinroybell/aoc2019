import sys


class State:
    def __init__(self, lines):
        self.objects = {}
        for line in lines:
            line = line.rstrip()
            obj = line.split(')')
            print(obj)
            if obj[0] not in self.objects:
                self.objects[obj[0]] = Node(obj[0])
            centre = self.objects[obj[0]]
            if obj[1] not in self.objects:
                self.objects[obj[1]] = Node(obj[1])
            orbiter = self.objects[obj[1]]

            orbiter.add_orbit(centre)

    def run_a(self):
        return self.objects["COM"].count_orbits(0)

    def run_b(self):
        return self.objects["COM"].parse_part_b(0).score


class PartBReturn:
    # In all cases, zero means unknown
    def __init__(self, score, you_level, santa_level):
        self.score = score
        self.you_level = you_level
        self.santa_level = santa_level

    def __str__(self):
        return "{} {} {}".format(self.score, self.you_level, self.santa_level)


class Node:
    def __init__(self, name):
        self.name = name
        self.sub = []
        self.orbits = None

    def add_orbit(self, orbits):
        self.orbits = orbits
        orbits.sub.append(self)

    def count_orbits(self, level):
        count = level
        for sub in self.sub:
            count += sub.count_orbits(level + 1)
        print(self.name, count)
        return count

    def parse_part_b(self, level):
        ret = PartBReturn(0, 0, 0)

        if (self.name == "YOU"):
            ret.you_level = level
        elif (self.name == "SAN"):
            ret.santa_level = level
        else:
            for sub in self.sub:
                sub_ret = sub.parse_part_b(level + 1)
                if sub_ret.score > 0:
                    # Done at a sub_level
                    return sub_ret
                if sub_ret.you_level > 0:
                    ret.you_level = sub_ret.you_level
                if sub_ret.santa_level > 0:
                    ret.santa_level = sub_ret.santa_level
                if ret.you_level > 0 and ret.santa_level > 0:
                    # This is the bottom point we need to get to
                    ret.score = ret.you_level + ret.santa_level - 2 * level - 2
                    return ret
        print(self.name, ret)
        return ret


def part_a(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    state = State(lines)
    return state.run_a()


def part_b(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    state = State(lines)
    return state.run_b()


def day6a():
    return part_a('data/day6.txt')


def day6b():
    return part_b('data/day6.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day6a())
    if 'b' in sys.argv:
        print(day6b())
