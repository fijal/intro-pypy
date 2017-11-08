
from rpython.jit.metainterp.test.support import LLJitMixin

from interp.lexer import get_lexer
from interp.parser import parser
from interp.interpreter import interpret

lexer = get_lexer()

class TestCompiled(LLJitMixin):
    def interp(self, p):
        def print_fn(arg):
            pass

        strings = [lexer.lex(p), None]

        def f(arg):
            ast = parser.parse(strings[arg])
            interpret(ast, print_fn)

        self.meta_interp(f, [0], listops=True)

    def test_loop(self):
        self.interp("""
fun main()
{
    i = 0;
    while i < 100 {
      i = i + 1;
    }
}        """)
