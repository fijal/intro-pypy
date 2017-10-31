
""" Usage: target-c file
"""

from interp.lexer import get_lexer
from interp.parser import parser
from interp.interpreter import interpret

lexer = get_lexer()

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
    interpret(ast)
    return 0

def target(*args):
    return main, None
