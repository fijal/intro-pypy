
""" Usage: target-c file
"""

from interp.lexer import get_lexer
from interp.parser import parser
from interp.interpreter import run
from interp.astnodes import Bytecode

lexer = get_lexer()

def printfn(obj):
    print obj.str()

def main(argv):
    if len(argv) != 2:
        print __doc__
        return 1
    try:
        contents = open(argv[1]).read()
    except OSError:
        print "Error reading " + argv[1]
        return 2
    ast = parser.parse(lexer.lex(contents))
    bc = Bytecode()
    ast.eval(bc)
    run(bc, printfn)
    return 0

def target(*args):
    return main, None
