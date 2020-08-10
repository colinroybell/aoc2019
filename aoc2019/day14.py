import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.sources = []
        self.touched = False
        self.created = 0
        self.amount = 0

    def create_ordering(self, nodes, ordering):
        if self.touched:
            return
        self.touched = True
        for source in self.sources:
            nodes[source[0]].create_ordering(nodes, ordering)
        ordering.append(self)
        return

    def process(self, nodes):
        recipes = (self.amount + self.created - 1) // self.created

        print("Making {} {} from ".format(self.created * recipes, self.name),
              end='')
        for source in self.sources:
            amount = recipes * source[1]
            print("{} {}, ".format(amount, source[0]), end='')
            nodes[source[0]].amount += amount
        print('')

    def __repr__(self):
        return self.name


def both_parts(filename, part):
    nodes = {}
    nodes['ORE'] = Node('ORE')
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            segs = line.split(' => ')
            created = segs[1].split(' ')
            name = created[1]
            node = Node(name)
            nodes[name] = node
            node.created = int(created[0])
            source_strings = segs[0].split(', ')
            for source_string in source_strings:
                source = source_string.split(' ')
                print(source)
                node.sources.append((source[1], int(source[0])))

    ordering = []
    nodes['FUEL'].create_ordering(nodes, ordering)
    print(ordering)

    nodes['FUEL'].amount = 1
    copy_ordering = ordering[:]

    if part == 'a':
        while ordering:
            node = ordering.pop()
            if node.name != 'ORE':
                node.process(nodes)
        return nodes['ORE'].amount

    min_ = 0
    max_ = 10**12

    while max_ - min_ > 1:
        mid = (max_ + min_) // 2
        for name in nodes:
            nodes[name].amount = 0
        nodes['FUEL'].amount = mid

        ordering = copy_ordering[:]
        while ordering:
            node = ordering.pop()
            if node.name != 'ORE':
                node.process(nodes)

        print(min_, max_, mid, nodes['ORE'].amount)

        if nodes['ORE'].amount < 10**12:
            min_ = mid
        else:
            max_ = mid

    return min_


def day14a():
    return both_parts('data/day14.txt', 'a')


def day14b():
    return both_parts('data/day14.txt', 'b')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day14a())
    if 'b' in sys.argv:
        print(day14b())
