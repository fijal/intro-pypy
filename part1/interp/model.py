
class Root(object):
    _attrs_ = [] # force the attributes on Root to be empty

class Integer(Root):
    def __init__(self, intval):
        self.intval = intval

    def str(self):
        return str(self.intval)

class Object(Root):
    def __init__(self):
        pass # type, etc
    
    def str(self):
        return "lonely object"

