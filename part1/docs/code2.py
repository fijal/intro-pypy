def f(x):
    return x

def entry_point(argv):
    print f(1) + f("foo")
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
