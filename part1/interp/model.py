class ReturnException(Exception):
    def __init__(self, retval):
        self.retval = retval

class Root(object):
    _attrs_ = [] # force the attributes on Root to be empty

class String(Root):
    def __init__(self, strval):
        self.strval = strval

    def is_true(self):
        return self.strval != ''

    def add(self, other):
        assert isinstance(other, String)
        return String(self.strval + other.strval)

    def equals(self, other):
        assert isinstance(other, String)
        return self.strval == other.strval

    def str(self):
        return self.strval

class Integer(Root):
    def __init__(self, intval):
        self.intval = intval

    def is_true(self):
        return self.intval != 0

    def add(self, other):
        if not isinstance(other, Integer):
            assert False
        return Integer(self.intval + other.intval)

    def equals(self, other):
        assert isinstance(other, Integer)
        return Integer(1 if self.intval == other.intval else 0)

    def lt(self, other):
        assert isinstance(other, Integer)
        return Integer(1 if self.intval < other.intval else 0)

    def str(self):
        return str(self.intval)

class ClassObj(Root):
    def __init__(self, name, arglist):
        self.name = name
        self.arglist = arglist

    def is_true(self):
        return True

    def str(self):
        return '<class %s>' % (self.name,)

    def call(self, frame, args):
        assert len(args) == len(self.arglist)
        frame.push(Object(self, args))

class Object(Root):
    def __init__(self, cls, values):
        self.cls = cls
        self.data = {}
        for i in range(len(values)):
            self.data[cls.arglist[i]] = values[i]

    def str(self):
        return "<%s object: %r>" % (self.cls.name, self.data)

    def is_true(self):
        return True

    def getattr(self, name):
        return self.data[name]

    def setattr(self, name, val):
        self.data[name] = val

class BuiltinWrapper(Root):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def call(self, frame, arg):
        assert len(arg) == 1
        frame.push(self.func(arg[0]))

class FunctionObj(Root):
    def __init__(self, name, arglist, body):
        self.name = name
        self.arglist = arglist
        self.body = body

    def call(self, frame, args):
        from interp.interpreter import Frame
        assert len(self.arglist) == len(args)
        f = Frame(frame)
        for i in range(0, len(args)):
            f.locals[self.arglist[i]] = args[i]
        try:
            for s in self.body:
                s.eval(f)
        except ReturnException as exc:
            frame.push(exc.retval)
        else:
            frame.push(Integer(0))
