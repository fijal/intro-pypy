
from rply.token import BaseBox
from interp.model import Integer, FunctionObj, ClassObj, ReturnException

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
        self.left.eval(frame)
        self.right.eval(frame)
        rightval = frame.pop()
        leftval = frame.pop()
        if self.op == "+":
            frame.push(leftval.add(rightval))
        elif self.op == '==':
            frame.push(leftval.equals(rightval))
        elif self.op == '<':
            frame.push(leftval.lt(rightval))
        else:
            assert False

class Return(AstNode):
    def __init__(self, elem):
        self.elem = elem

    def eval(self, frame):
        self.elem.eval(frame)
        raise ReturnException(frame.pop())

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
        frame.locals[self.name] = FunctionObj(self.name, self.arglist, self.body)

class If(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list

    def eval(self, frame):
        self.expr.eval(frame)
        if frame.pop().is_true():
            for s in self.stmt_list:
                s.eval(frame)

class DottedExpr(AstNode):
    def __init__(self, atom, ident):
        self.atom = atom
        self.ident = ident

    def eval(self, frame):
        self.atom.eval(frame)
        obj = frame.pop()
        frame.push(obj.getattr(self.ident))

class Atom(AstNode):
    def __init__(self, name):
        self.name = name

    def eval(self, frame):
        frame.push(frame.getlocal(self.name))

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
        obj.setattr(self.v, frame.pop())

class While(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list

    def eval(self, frame):
        self.expr.eval(frame)
        while frame.pop().is_true():
            for s in self.stmt_list:
                s.eval(frame)
            self.expr.eval(frame)

class Class(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def eval(self, frame):
        frame.locals[self.name] = ClassObj(self.name, self.arglist)

class Call(AstNode):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def eval(self, frame):
        args = []
        for a in self.arglist:
            a.eval(frame)
            args.append(frame.pop())
        frame.getlocal(self.name).call(frame, args)
