import sys


def part_a(filename):
    f = open(filename, 'r')
    line = f.readline()
    f.close()

    line = line.rstrip()
    assert(len(line) % 150 == 0)
    min_zero = 150
    score = 0
    for layer in range(0, len(line) // 150):
        counts = [0] * 3
        for i in range(0, 150):
            counts[int(line[layer * 150 + i])] += 1

        print(counts)

        if counts[0] < min_zero:
            min_zero = counts[0]
            score = counts[1] * counts[2]

    return score

def part_b(filename):
    f = open(filename, 'r')
    line = f.readline()
    f.close()

    line = line.rstrip()
    assert(len(line) % 150 == 0)

    image = [2]*150

    for layer in range(0, len(line) // 150):
        for i in range(0, 150):
            if image[i] == 2:
                image[i] = int(line[layer * 150 + i])

    i = 0
    for y in range(0,6):
        for x in range(0,25):
            char = "#"
            if image[i] == 0:
                char = "."
            print(char,end='')
            i += 1
        print("")

    return None


def day8a():
    return part_a('data/day8.txt')


def day8b():
    return part_b('data/day8.txt')


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day8a())
    if 'b' in sys.argv:
        print(day8b())
