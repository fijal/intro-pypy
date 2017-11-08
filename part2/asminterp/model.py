
class Base(object):
    pass

class Integer(Base):
    def __init__(self, intval):
        self.intval = intval

    def sub(self, other):
        assert isinstance(other, Integer)
        return Integer(self.intval - other.intval)

    def add(self, other):
        assert isinstance(other, Integer)
        return Integer(self.intval + other.intval)

    def lt(self, other):
        assert isinstance(other, Integer)
        return Integer(self.intval < other.intval)            

    def is_true(self):
        return self.intval != 0

    def repr(self):
        return str(self.intval)
