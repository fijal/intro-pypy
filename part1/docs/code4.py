
from rpython.rlib.objectmodel import specialize

@specialize.argtype(0)
def f(arg):
    if isinstance(arg, int):
        return arg + 13
    elif isinstance(arg, str):
        return len(arg)

def entry_point(argv):
    print f(1) + f("foo")
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
