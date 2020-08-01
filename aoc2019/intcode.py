class State:
    def __init__(self, string):
        self.pc = 0
        self.done = 0
        string.rstrip()
        data = string.split(',')
        self.mem = []
        for datum in data:
            self.mem.append(int(datum))

    def check_bound(self, i):
        assert(i >= 0 and i < len(self.mem))

    def get_immediate(self, i):
        self.check_bound(i)
        return self.mem[i]

    def set_immediate(self, i, v):
        self.check_bound(i)
        self.mem[i] = v

    def get_position(self, i):
        self.check_bound(i)
        self.check_bound(self.mem[i])
        return self.mem[self.mem[i]]

    def set_position(self, i, v):
        self.check_bound(i)
        self.check_bound(self.mem[i])
        self.mem[self.mem[i]] = v

    def get(self, i, mode):
        if mode:
            return self.get_immediate(i)
        else:
            return self.get_position(i)

    def set_(self, i, v, mode):
        if mode:
            self.set_immediate(i, v)
        else:
            self.set_position(i, v)

    def run(self):
        while not self.done:
            self.check_bound(self.pc)
            instruction = self.get_immediate(self.pc)
            print(self.pc, instruction)
            op_code = instruction % 100
            assert(op_code in dispatch)
            dispatch[op_code](self, instruction)
        return self.get_immediate(0)


def get_modes(instruction):
    A = instruction // 10000
    B = (instruction // 1000) % 10
    C = (instruction // 100) % 10
    return (C, B, A)


def add(state, instruction):
    ''' Op 1: add '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    b = state.get(state.pc, mode[1])
    state.pc += 1
    state.set_(state.pc, a + b, mode[2])
    state.pc += 1


def multiply(state, instruction):
    ''' Op 2: multiply '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    b = state.get(state.pc, mode[1])
    state.pc += 1
    state.set_(state.pc, a * b, mode[2])
    state.pc += 1


def input_(state, instruction):
    ''' Op3: input '''
    state.pc += 1
    a = state.get_immediate(state.pc)
    value = int(input("Input needed: "))
    state.set_immediate(a, value)
    state.pc += 1


def output(state, instruction):
    ''' Op4: output '''
    mode = get_modes(instruction)
    state.pc += 1
    value = state.get(state.pc, 0)
    print("Output {}".format(value))
    state.pc += 1


def jump_if_true(state, instruction):
    ''' Op 5 '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    if a:
        state.pc = state.get(state.pc, mode[1])
    else:
        state.pc += 1


def jump_if_false(state, instruction):
    ''' Op 6 '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    if not a:
        state.pc = state.get(state.pc, mode[1])
    else:
        state.pc += 1


def less_than(state, instruction):
    ''' Op 7 '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    b = state.get(state.pc, mode[1])
    state.pc += 1
    if a < b:
        v = 1
    else:
        v = 0
    state.set_(state.pc, v, mode[2])
    state.pc += 1


def equals(state, instruction):
    ''' Op 8 '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.pc += 1
    b = state.get(state.pc, mode[1])
    state.pc += 1
    if a == b:
        v = 1
    else:
        v = 0
    state.set_(state.pc, v, mode[2])
    state.pc += 1


def stop(state, instruction):
    ''' Op 99: stop '''
    state.done = 1
    state.pc += 1


dispatch = {
    1: add,
    2: multiply,
    3: input_,
    4: output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: stop
}
