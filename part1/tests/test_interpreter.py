
from interp.parser import parser
from interp.lexer import get_lexer
from interp.interpreter import interpret

class TestInterpreter(object):
    def setup_method(self, meth):
        self.printed = []

    def interp(self, code):
        def printfn(w_obj):
            self.printed.append(w_obj)

        interpret(parser.parse(get_lexer().lex(code)), printfn)
        return self.printed
    
    def test_basic(self):
        p = self.interp("""
          fun main() {
              print(13);
          }
        """)
        assert p[0].intval == 13

