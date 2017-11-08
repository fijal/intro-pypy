
from interp.model import Integer

class Frame(object):
    next = None

    def __init__(self, printfn):
        self.locals = {}
        self.stack = []
        self.printfn = printfn

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def enter(self):
        f = Frame(self.printfn)
        f.globals = self.globals
        return f

def interpret(ast, printfn):
    ast.eval(Frame(printfn))
