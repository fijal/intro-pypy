
from interp.model import Integer, BuiltinWrapper

class Frame(object):
    def __init__(self, parent):
        self.parent = parent
        self.locals = {}
        self.stack = []

    def getlocal(self, name):
        p = self
        while p is not None and name not in p.locals:
            p = p.parent
        assert p is not None, "Failed to lookup '%s'" % (name,)
        return p.locals[name]

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

def interpret(ast, printfn):
    f = Frame(None)
    f.locals['print'] = BuiltinWrapper('printfn', printfn)
    ast.eval(f)
    f.getlocal('main').call(f, [])
