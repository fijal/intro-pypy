
from asminterp.parser import parse, repr_bytecode
from asminterp import interp1, interp2, interp3

def print_fn(arg):
    print arg

def main(argv):
    if len(argv) != 2 and len(argv) != 3:
        print __doc__
        return 1
    try:
        contents = open(argv[1]).read()
    except OSError:
        print "Error reading " + argv[1]
        return 2
    engine = interp1.interp
    if len(argv) == 3:
        if argv[2] == "1":
            engine = interp1.interp
        elif argv[2] == "2":
            engine = interp2.interp
        elif argv[2] == "3":
            engine = interp3.interp
        elif argv[2] == "print":
            print repr_bytecode(parse(contents))
            return 0
    engine(parse(contents), print_fn)
    return 0

def target(*args):
    return main, None
