
from rpython.rlib.objectmodel import specialize

def new_f():
    def f(arg):
        if isinstance(arg, int):
            return arg + 13
        elif isinstance(arg, str):
            return len(arg)
    return f

int_f = new_f()
str_f = new_f()

def entry_point(argv):
    print int_f(1) + str_f("foo")
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
