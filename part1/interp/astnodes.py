
from rply.token import BaseBox
from interp.model import Integer

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
        for item in self.lst:
            item.eval(frame)

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
        if self.op == "+":
            self.left.eval(frame)
            self.right.eval(frame)
            rightval = frame.pop()
            leftval = frame.pop()
            frame.push(leftval.add(rightval))
            return
        assert False

class Return(AstNode):
    def __init__(self, elem):
        self.elem = elem

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

    def eval(self, frame):
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

class While(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list

class Class(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

class Call(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def eval(self, frame):
        assert self.name == 'print'
        elem = self.arglist[0].eval(frame)
        frame.printfn(frame.stack[-1])


