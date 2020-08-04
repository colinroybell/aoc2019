class State:
    def __init__(self, string, name="anon", input_pipe=None,
                 output_pipe=None, debug=0):
        self.pc = 0
        self.done = 0
        self.name = name
        self.input_pipe = input_pipe
        self.output_pipe = output_pipe
        self.debug = debug
        self.relative_base = 0
        string.rstrip()
        data = string.split(',')
        self.mem = []
        for datum in data:
            self.mem.append(int(datum))

    def check_bound(self, i):
        assert(i >= 0)
        if i >= len(self.mem):
            self.mem.extend([0]*(i + 1 -len(self.mem)))

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

    def get_relative(self, i):
        self.check_bound(i)
        self.check_bound(self.mem[i] + self.relative_base)
        return self.mem[self.mem[i] + self.relative_base]

    def set_position(self, i, v):
        self.check_bound(i)
        self.check_bound(self.mem[i])
        self.mem[self.mem[i]] = v

    def set_relative(self, i, v):
        self.check_bound(i)
        self.check_bound(self.mem[i] + self.relative_base)
        self.mem[self.mem[i] + self.relative_base] = v

    def get(self, i, mode):
        if mode == 0:
            return self.get_position(i)
        elif mode == 1:
            return self.get_immediate(i)
        elif mode == 2:
            return self.get_relative(i)

    def set_(self, i, v, mode):
        if mode == 0:
            self.set_position(i, v)
        elif mode == 1:
            self.set_immediate(i, v)
        elif mode == 2:
            self.set_relative(i,v)

    def run(self):
        while not self.done:
            self.run_one_step()
        return self.get_immediate(0)

    def run_one_step(self):
        if not self.done:
            self.check_bound(self.pc)
            instruction = self.get_immediate(self.pc)
            op_code = instruction % 100
            assert(op_code in dispatch)
            dispatch[op_code](self, instruction)
        return self.done


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
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, 1)
    if state.input_pipe is not None:
        if len(state.input_pipe):
            value = state.input_pipe.pop(0)
            if state.debug:
                print("{} read {}".format(state.name, value))
        else:
            if state.debug:
                print("{} blocking".format(state.name))
            state.pc -= 1
            return
    else:
        value = int(input("Input needed: "))
    state.set_immediate(a + state.relative_base, value)
    state.pc += 1


def output(state, instruction):
    ''' Op4: output '''
    mode = get_modes(instruction)
    state.pc += 1
    value = state.get(state.pc, mode[0])
    if state.output_pipe is not None:
        state.output_pipe.append(value)
        if state.debug:
            print("{} wrote {}".format(state.name, value))
    else:
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

def change_relative_base(state, instruction):
    ''' Op 9 '''
    mode = get_modes(instruction)
    state.pc += 1
    a = state.get(state.pc, mode[0])
    state.relative_base += a
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
    9: change_relative_base,
    99: stop
}
