
from interp.model import Integer

class Frame(object):
    def __init__(self, printfn):
        self.locals = {}
        self.stack = []
        self.printfn = printfn

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

def interpret(ast, printfn):
    ast.eval(Frame(printfn))
