import sys
from intcode import State
import itertools


my_string = "3,8,1001,8,10,8,105,1,0,0,21,46,67,76,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,4,9,9,102,3,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99"


def part_a(string):
    inputs = [0, 1, 2, 3, 4]
    max_output = 0
    for input_ in itertools.permutations(inputs):
        pipes = []
        for i in range(0, 6):
            pipes.append([])

        states = []
        for i in range(0, 5):
            states.append(State(string, name="Amp" + str(i + 1),
                          input_pipe=pipes[i], output_pipe=pipes[i + 1],
                          debug=0))

        print("input {}".format(input_))
        for i in range(0, 5):
            pipes[i].append(input_[i])
        pipes[0].append(0)
        print(pipes[0])

        done = 0
        while not done:
            done = 1
            for state in states:
                ret = state.run_one_step()
                if ret == 0:
                    done = 0

        print(pipes)

        output = pipes[5].pop(0)

        if output > max_output:
            max_output = output
    return max_output


def part_b(string):
    inputs = [5, 6, 7, 8, 9]
    max_output = 0
    for input_ in itertools.permutations(inputs):
        pipes = []
        for i in range(0, 5):
            pipes.append([])

        states = []
        for i in range(0, 5):
            states.append(State(string, name="Amp"+str(i + 1),
                          input_pipe=pipes[i], output_pipe=pipes[(i + 1) % 5],
                          debug=0))

        print("input {}".format(input_))
        for i in range(0, 5):
            pipes[i].append(input_[i])
        pipes[0].append(0)
        print(pipes[0])

        done = 0
        while not done:
            done = 1
            for state in states:
                ret = state.run_one_step()
                if ret == 0:
                    done = 0

        print(pipes)

        output = pipes[0].pop(0)

        if output > max_output:
            max_output = output
    return max_output


def day7a():
    return part_a(my_string)


def day7b():
    return part_b(my_string)


if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day7a())
    if 'b' in sys.argv:
        print(day7b())
