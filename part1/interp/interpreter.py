
from rpython.rlib.jit import JitDriver, promote

from interp.model import Integer, NoneObject
from interp import opcodes

class Frame(object):
    next = None

    def __init__(self, nlocals):
        self.locals = [None] * nlocals
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def setlocal(self, no, value):
        self.locals[no] = value

    def getlocal(self, no):
        return self.locals[no]

def run(bc, printfn):
    interpreter = Interpreter(bc, printfn)
    interpreter.interpret(bc.codes['main'])

def printable_loc(i, bc, interp):
    return "POS:" + str(i)

driver = JitDriver(greens = ['i', 'bc', 'self'], reds = ['frame'],
                   get_printable_location=printable_loc)

class Interpreter(object):
    _immutable_fields_ = ['bc']

    def __init__(self, bc, printfn):
        self.bc = bc
        self.printfn = printfn

    def interpret(self, func):
        bc = func.code
        frame = Frame(func.nlocals)
        i = 0
        while i < len(bc):
            driver.jit_merge_point(i=i, bc=bc, frame=frame, self=self)
            code = ord(bc[i])
            i += 1
            arg0 = 0
            arg1 = 0
            if code >= 100:
                arg0 = ord(bc[i])
                i += 1
            if code >= 200:
                arg1 = ord(bc[i])
                i += 1
            if code == opcodes.DISCARD:
                frame.pop()
            elif code == opcodes.ASSIGN:
                self.assign(frame, arg0)
            elif code == opcodes.LT:
                self.lt(frame)
            elif code == opcodes.LOAD_NAME:
                self.load_name(frame, arg0)
            elif code == opcodes.ADD:
                self.add(frame)
            elif code == opcodes.CALL:
                self.call(frame, self.bc.names[arg0], arg1)
            elif code == opcodes.LOAD_INTEGER:
                frame.push(Integer(arg0))
            elif code == opcodes.JUMP_IF_FALSE:
                val = frame.pop()
                if not val.is_true():
                    i = arg0
            elif code == opcodes.JUMP_ABSOLUTE:
                i = arg0
                driver.can_enter_jit(i=i, bc=bc, frame=frame, self=self)
            else:
                print "opcode " + str(code) + " not implemented"
                raise Exception("unimplemented opcode " + str(code))

    def add(self, frame):
        right = frame.pop()
        left = frame.pop()
        frame.push(left.add(right))

    def lt(self, frame):
        right = frame.pop()
        left = frame.pop()
        frame.push(left.lt(right))

    def assign(self, frame, no):
        frame.setlocal(no, frame.pop())

    def load_name(self, frame, no):
        frame.push(frame.getlocal(no))

    def call(self, frame, funcname, numargs):
        if funcname == 'print':
            assert numargs == 1
            self.printfn(frame.pop())
            frame.push(NoneObject())
            return
        raise Exception("calling unimplemented")
