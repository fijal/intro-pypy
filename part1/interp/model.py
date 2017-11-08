
class Root(object):
    _attrs_ = [] # force the attributes on Root to be empty

class Integer(Root):
    def __init__(self, intval):
        self.intval = intval

    def add(self, other):
        if not isinstance(other, Integer):
            assert False
        return Integer(self.intval + other.intval)

    def lt(self, other):
        assert isinstance(other, Integer)
        return Integer(self.intval < other.intval)

    def is_true(self):
        return self.intval != 0

    def str(self):
        return str(self.intval)

class Object(Root):
    def __init__(self, d):
        self.d = d
    
    def str(self):
        return "lonely object"

    def getitem(self, item):
        return self.d[item]

    def setitem(self, item, v):
        self.d[item] = v
