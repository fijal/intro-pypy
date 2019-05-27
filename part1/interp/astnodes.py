
from rply.token import BaseBox
from interp.model import Integer, Object
from interp import opcodes

from rpython.rlib import jit

driver = jit.JitDriver(greens=["i", "self", "stmt"], reds=["frame"], is_recursive=True)

class FunctionCode(object):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

class Bytecode(object):
    _immutable_fields_ = ['names']

    def __init__(self):
        self.codes = {}
        self.names = []
        self.name_lookup = {}

    def new_function(self, name, arglist):
        self.codes[name] = FunctionCode(name, arglist)
        self.current_function = self.codes[name]
        self.current_code = []

    def end_current_function(self):
        self.current_function.code = "".join(self.current_code)
        self.current_function.nlocals = len(self.names)
        self.current_function = None

    def register_name(self, name):
        try:
            return self.name_lookup[name]
        except KeyError:
            pass
        self.names.append(name)
        self.name_lookup[name] = len(self.names) - 1
        return len(self.names) - 1

    def get_name(self, no):
        assert no <= 255
        return self.names[no]

    def get_pos(self):
        return len(self.current_code)
    
    def patch_pos(self, loc, new_pos):
        self.current_code[loc] = chr(new_pos)

    def emit0(self, opnum):
        assert 0 <= opnum <= 255
        self.current_code.append(chr(opnum))

    def emit1(self, opnum, arg0):
        assert 0 <= opnum <= 255
        assert 0 <= arg0 <= 255
        self.current_code.append(chr(opnum))
        self.current_code.append(chr(arg0))

    def emit2(self, opnum, arg0, arg1):
        assert 0 <= opnum <= 255
        assert 0 <= arg0 <= 255
        assert 0 <= arg1 <= 255
        self.current_code.append(chr(opnum))
        self.current_code.append(chr(arg0))
        self.current_code.append(chr(arg1))

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
        self.lst = lst[:]

    def eval(self, bc):
        for elem in self.lst:
            elem.eval(bc)

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

    def eval(self, bc):
        bc.emit1(opcodes.LOAD_INTEGER, self.intval)

class BinOp(AstNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, bc):
        self.left.eval(bc)
        self.right.eval(bc)
        if self.op == '+':
            bc.emit0(opcodes.ADD)
        elif self.op == '<':
            bc.emit0(opcodes.LT)
        else:
            raise Exception("Not implemented")

class Exit(Exception):
    def __init__(self, val):
        self.val = val

class Return(AstNode):
    def __init__(self, elem):
        self.elem = elem

class Discard(AstNode):
    def __init__(self, expr):
        self.expr = expr
    
    def eval(self, bc):
        self.expr.eval(bc)
        bc.emit0(opcodes.DISCARD)

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

    def eval(self, bc):
        bc.new_function(self.name, self.arglist)
        for elem in self.body:
            print elem
            elem.eval(bc)
        bc.end_current_function()

    def getname(self):
        return self.name

class If(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list[:]

    def eval(self, bc):
        self.expr.eval(bc)
        pos1 = bc.get_pos()
        bc.emit1(opcodes.JUMP_IF_FALSE, 0)
        for stmt in self.stmt_list:
            stmt.eval(bc)
        bc.patch_pos(pos1 + 1, bc.get_pos())

class DottedExpr(AstNode):
    def __init__(self, atom, ident):
        self.atom = atom
        self.ident = ident

class Atom(AstNode):
    def __init__(self, name):
        self.name = name

    def eval(self, bc):
        bc.emit1(opcodes.LOAD_NAME, bc.register_name(self.name))

class Assign(AstNode):
    def __init__(self, v, expr):
        self.v = v
        self.expr = expr

    def eval(self, bc):
        self.expr.eval(bc)
        bc.emit1(opcodes.ASSIGN, bc.register_name(self.v))

class DottedAssign(AstNode):
    def __init__(self, atom, v, expr):
        self.atom = atom
        self.v = v
        self.expr = expr

class While(AstNode):
    def __init__(self, expr, stmt_list):
        self.expr = expr
        self.stmt_list = stmt_list[:]

    def eval(self, bc):
        pos0 = bc.get_pos()
        self.expr.eval(bc)
        pos1 = bc.get_pos()
        bc.emit1(opcodes.JUMP_IF_FALSE, 0)
        for stmt in self.stmt_list:
            stmt.eval(bc)
        bc.emit1(opcodes.JUMP_ABSOLUTE, pos0)
        bc.patch_pos(pos1 + 1, bc.get_pos())

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

    def eval(self, bc):
        for arg in self.arglist:
            arg.eval(bc)
        no = bc.register_name(self.name)
        bc.emit2(opcodes.CALL, no, len(self.arglist))

