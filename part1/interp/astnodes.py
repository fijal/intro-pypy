
from rply.token import BaseBox
from interp.model import Integer, Object

from rpython.rlib import jit

driver = jit.JitDriver(greens=["i", "self", "stmt"], reds=["frame"], is_recursive=True)


class AstNode(BaseBox):
    def __eq__(self, other):
        # not rpython, just for tests
        return self.__class__ is other.__class__ and self.__dict__ == other.__dict__

    def __repr__(self):
        # Not rpython, debugging only
        d = " ".join(["%s=%r" % (k, v) for k, v in sorted(self.__dict__.iteritems())])
        return '<%s %s>' % (self.__class__.__name__, d)

    def eval(self, frame):
        raise Exception("unimplemented")

class Program(AstNode):
    def __init__(self, lst):
        self.lst = lst[:]

class ArgumentList(AstNode):
    _immutable_fields_ = ['elem', 'next']
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
    _immutable_fields_ = ['v']
    def __init__(self, v):
        self.intval = v

class BinOp(AstNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Exit(Exception):
    def __init__(self, val):
        self.val = val

class Return(AstNode):
    def __init__(self, elem):
        self.elem = elem

class Discard(AstNode):
    def __init__(self, expr):
        self.expr = expr

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
        self.arglist = arglist[:]
        self.body = body[:]

    def getname(self):
        return self.name

class If(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list[:]

class DottedExpr(AstNode):
    def __init__(self, atom, ident):
        self.atom = atom
        self.ident = ident

class Atom(AstNode):
    def __init__(self, name):
        self.name = name

class Assign(AstNode):
    def __init__(self, v, expr):
        self.v = v
        self.expr = expr

class DottedAssign(AstNode):
    def __init__(self, atom, v, expr):
        self.atom = atom
        self.v = v
        self.expr = expr

class While(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list[:]

class Class(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist[:]

    def getname(self):
        return self.name

class Call(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist[:]
