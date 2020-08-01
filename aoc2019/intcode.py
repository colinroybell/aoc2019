class State:
    def __init__ (self, string):
        self.pc = 0
        self.done = 0
        string.rstrip()
        data = string.split(',')
        self.mem = []
        for datum in data:
            self.mem.append(int(datum))

    def check_bound(self, i):
        assert(i >=0 and i < len(self.mem))

    def get(self,i):
        self.check_bound(i)
        return self.mem[i]

    def get_indirect(self, i):
        self.check_bound(i)
        self.check_bound(self.mem[i])
        return self.mem[self.mem[i]]

    def set_indirect(self, i, v):
        self.check_bound(i)
        self.check_bound(self.mem[i])
        self.mem[self.mem[i]] = v

    def run(self):
        while not self.done:
            op_code = self.get(self.pc)
            assert(op_code in dispatch)
            dispatch[op_code](self)
        return self.get(0)

def add(state):
    ''' Op 1: add '''
    state.pc += 1
    a = state.get_indirect(state.pc)
    state.pc += 1
    b = state.get_indirect(state.pc)
    state.pc += 1
    state.set_indirect(state.pc, a + b)
    state.pc += 1

def multiply(state):
    ''' Op 2: multiply '''
    state.pc += 1
    a = state.get_indirect(state.pc)
    state.pc += 1
    b = state.get_indirect(state.pc)
    state.pc += 1
    state.set_indirect(state.pc, a * b)
    state.pc += 1

def stop(state):
    ''' Op 99: stop '''
    state.done = 1
    state.pc += 1



dispatch = {
    1: add,
    2: multiply,
    99: stop
}
