
from rpython.rlib import jit

from asminterp import parser as p
from asminterp.model import Integer

driver = jit.JitDriver(greens=["i", "bc", "bytecode"], reds=["f"],
    virtualizables=["f"], is_recursive=True)

class Frame(object):
    _virtualizable_ = ['stack[*]', 'locals[*]', 'stack_depth']

    def __init__(self):
        self.stack = [None] * 15
        self.locals = [None] * 15
        self.stack_depth = 0

    def append(self, v):
        self.stack[self.stack_depth] = v
        self.stack_depth += 1

    def pop(self):
        idx = self.stack_depth - 1
        assert idx >= 0
        self.stack_depth = idx
        return self.stack[idx]

def interp(bytecode, print_fn):
    i = 0
    f = Frame()
    bc = bytecode.bc
    while i < len(bc):
        driver.jit_merge_point(bc=bc, bytecode=bytecode, i=i, f=f)
        code = ord(bc[i])
        arg0 = ord(bc[i + 1])
        arg1 = ord(bc[i + 2])
        if code == p.LOAD_INTEGER:
            f.append(Integer(arg0))
        elif code == p.LOAD_CONSTANT:
            f.append(bytecode.consts[arg0])
        elif code == p.STORE:
            f.locals[arg0] = f.pop()
        elif code == p.LOAD:
            f.append(f.locals[arg0])
        elif code == p.SUB:
            right = f.pop()
            left = f.pop()
            f.append(left.sub(right))
        elif code == p.ADD:
            right = f.pop()
            left = f.pop()
            f.append(left.add(right))            
        elif code == p.JUMP_IF_FALSE:
            val = f.pop()
            if not val.is_true():
                i = arg0 * 3
                continue
        elif code == p.JUMP:
            i = arg0 * 3
            continue
        elif code == p.PRINT:
            print_fn(f.pop().repr())
        else:
            print("Unknown bytecode %d" % code)
            raise Exception("unknown bytecode %s" % p.OPCODES[code])
        i += 3
