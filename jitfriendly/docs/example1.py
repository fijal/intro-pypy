
# attribute access
class X(object):
    def __init__(self):
        self.foo = 13

x = X()

x.foo # fast
getattr(x, 'foo') # still fast!
foo = 'foo'
getattr(x, foo) # slow

# function call
def f(a, b, c):
    pass

f(1, 2, 3) # good
f(a=1, b=2, c=3) # still good
f(**{'a': 1, 'b': 2, 'c': 3}) # still ok if you are lucky
import json
f(**json.loads('{"a": 1, "b": 2, "c": 3}')) # out of luck

# function declaration

def f(a, b, c):
    pass # good

def f(a, b, c):
    def g(a, b): # still ok
        pass

def f(a, b, c):
    exec """def g(a, b): pass""" # bad

def f(a, b, c):
    class X(object):
        pass # terrible

