
from rply.token import BaseBox
from interp.model import Integer, Object

from rpython.rlib import jit

driver = jit.JitDriver(greens=["self"], reds=["frame"], is_recursive=True)


class AstNode(BaseBox):
    def __eq__(self, other):
        # not rpython, just for tests
        return self.__class__ is other.__class__ and self.__dict__ == other.__dict__

    def __repr__(self):
        # Not rpython, debugging only
        d = " ".join(["%s=%r" % (k, v) for k, v in sorted(self.__dict__.iteritems())])
        return '<%s %s>' % (self.__class__.__name__, d)

class Program(AstNode):
    def __init__(self, lst):
        self.lst = lst

    def eval(self, frame):
        d = {}
        for item in self.lst:
            d[item.getname()] = item
        frame.globals = d
        d['main'].call(frame)

class ArgumentList(AstNode):
    def __init__(self, elem, next):
        self.v = elem
        self.next = next

    def get_arg_list(self):
        """ returns list of strings
        """
        lst = []
        cur = self
        while cur.v is not None:
            lst.append(cur.v)
            cur = cur.next
            assert isinstance(cur, ArgumentList)
            # ^^^ crucial, otherwise can be BaseBox and cur.next would explode
        return lst

class AstInteger(AstNode):
    def __init__(self, v):
        self.intval = v

    def eval(self, frame):
        frame.push(Integer(self.intval))

class BinOp(AstNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, frame):
        self.left.eval(frame)
        self.right.eval(frame)
        rightval = frame.pop()
        leftval = frame.pop()
        if self.op == "+":
            frame.push(leftval.add(rightval))
        elif self.op == "<":
            frame.push(leftval.lt(rightval))
        else:
            assert False

class Exit(Exception):
    def __init__(self, val):
        self.val = val

class Return(AstNode):
    def __init__(self, elem):
        self.elem = elem

    def eval(self, frame):
        self.elem.eval(frame)
        raise Exit(frame.pop())

class Discard(AstNode):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, frame):
        self.expr.eval(frame)
        frame.pop()

class StatementList(AstNode):
    def __init__(self, elem, next):
        self.elem = elem
        self.next = next

    def get_elem_list(self):
        """ returns list of AstNodes
        """
        lst = []
        cur = self
        while cur.elem is not None:
            lst.append(cur.elem)
            cur = cur.next
            assert isinstance(cur, StatementList)
            # ^^^ crucial, otherwise can be BaseBox and cur.next would explode
        return lst

class Function(AstNode):
    def __init__(self, name, arglist, body):
        self.name = name
        self.arglist = arglist
        self.body = body

    def getname(self):
        return self.name

    def call(self, frame):
        for i in range(len(self.arglist) - 1, -1, -1):
            frame.locals[self.arglist[i]] = frame.pop()
        for elem in self.body:
            elem.eval(frame)

class If(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list

class DottedExpr(AstNode):
    def __init__(self, atom, ident):
        self.atom = atom
        self.ident = ident

    def eval(self, frame):
        self.atom.eval(frame)
        obj = frame.pop()
        frame.push(obj.getitem(self.ident))

class Atom(AstNode):
    def __init__(self, name):
        self.name = name

    def eval(self, frame):
        frame.push(frame.locals[self.name])

class Assign(AstNode):
    def __init__(self, v, expr):
        self.v = v
        self.expr = expr

    def eval(self, frame):
        self.expr.eval(frame)
        frame.locals[self.v] = frame.pop()

class DottedAssign(AstNode):
    def __init__(self, atom, v, expr):
        self.atom = atom
        self.v = v
        self.expr = expr

    def eval(self, frame):
        self.atom.eval(frame)
        obj = frame.pop()
        self.expr.eval(frame)
        val = frame.pop()
        obj.setitem(self.v, val)

class While(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list

    def eval(self, frame):
        while True:
            driver.jit_merge_point(self=self, frame=frame)
            self.expr.eval(frame)
            if not frame.pop().is_true():
                return
            for stmt in self.stmt_list:
                stmt.eval(frame)

class Class(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def getname(self):
        return self.name

    def call(self, frame):
        d = {}
        for i in range(len(self.arglist) -1, -1, -1):
            d[self.arglist[i]] = frame.pop()
        raise Exit(Object(d))

class Call(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def eval(self, frame):
        if self.name == 'print':
            self.arglist[0].eval(frame)
            frame.printfn(frame.stack[-1])
        else:
            try:
                newframe = frame.enter()
                for arg in self.arglist:
                    arg.eval(newframe)
                frame.globals[self.name].call(newframe)
            except Exit as e:
                val = e.val
            else:
                val = Integer(0)
            frame.push(val)
