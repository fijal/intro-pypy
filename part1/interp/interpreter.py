
from interp.model import Integer, NoneObject
from interp import opcodes

class Frame(object):
    next = None

    def __init__(self):
        self.locals = {}
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def setlocal(self, name, value):
        self.locals[name] = value

    def getlocal(self, name):
        return self.locals[name]

def run(bc, printfn):
    interpreter = Interpreter(bc, printfn)
    interpreter.interpret(bc.codes['main'])


class Interpreter(object):
    def __init__(self, bc, printfn):
        self.bc = bc
        self.printfn = printfn

    def interpret(self, func):
        bc = func.code
        frame = Frame()
        i = 0
        arg0 = 0
        arg1 = 0
        while i < len(bc):
            code = ord(bc[i])
            i += 1
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
        name = self.bc.get_name(no)
        frame.setlocal(name, frame.pop())

    def load_name(self, frame, no):
        name = self.bc.get_name(no)
        frame.push(frame.getlocal(name))

    def call(self, frame, funcname, numargs):
        if funcname == 'print':
            assert numargs == 1
            self.printfn(frame.pop())
            frame.push(NoneObject())
            return
        raise Exception("calling unimplemented")
