
from rpython.rlib import jit

from asminterp import parser as p
from asminterp.model import Integer

driver = jit.JitDriver(greens=["i", "bc", "bytecode"], reds=["locals", "stack"])

def interp(bytecode, print_fn):
    i = 0
    stack = []
    locals = [None] * 256
    bc = bytecode.bc
    while i < len(bc):
        driver.jit_merge_point(bc=bc, i=i, locals=locals, stack=stack,
                               bytecode=bytecode)
        code = ord(bc[i])
        arg0 = ord(bc[i + 1])
        arg1 = ord(bc[i + 2])
        if code == p.LOAD_INTEGER:
            stack.append(Integer(arg0))
        elif code == p.LOAD_CONSTANT:
            stack.append(bytecode.consts[arg0])
        elif code == p.STORE:
            locals[arg0] = stack.pop()
        elif code == p.LOAD:
            stack.append(locals[arg0])
        elif code == p.SUB:
            right = stack.pop()
            left = stack.pop()
            stack.append(left.sub(right))
        elif code == p.ADD:
            right = stack.pop()
            left = stack.pop()
            stack.append(left.add(right))            
        elif code == p.JUMP_IF_FALSE:
            val = stack.pop()
            if not val.is_true():
                i = arg0 * 3
                continue
        elif code == p.JUMP:
            i = arg0 * 3
            driver.can_enter_jit(bc=bc, i=i, locals=locals, stack=stack,
                                 bytecode=bytecode)
            continue
        elif code == p.PRINT:
            print_fn(stack.pop().repr())
        else:
            print("Unknown bytecode %d" % code)
            raise Exception("unknown bytecode %s" % p.OPCODES[code])
        i += 3
