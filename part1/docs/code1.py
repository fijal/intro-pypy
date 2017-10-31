
def fib(n):
    if n == 0 or n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

def entry_point(argv):
    if len(argv) < 2:
        print "not enough arguments"
        return 1
    print fib(int(argv[1]))
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
