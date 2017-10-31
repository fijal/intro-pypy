
def entry_point(argv):
    l = []
    l.append(1)
    l.append("foo")
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
