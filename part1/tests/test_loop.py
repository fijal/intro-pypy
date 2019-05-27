
from rpython.jit.metainterp.test.support import LLJitMixin

from interp.lexer import get_lexer
from interp.parser import parser
from interp.jit_interpreter import run
from interp.astnodes import Bytecode

lexer = get_lexer()

p = "fun main() {}"

ast = parser.parse(lexer.lex(p))
one_more_bc = Bytecode()
ast.eval(one_more_bc)


class TestCompiled(LLJitMixin):
    def interp(self, p):
        def print_fn(arg):
            pass

        ast = parser.parse(lexer.lex(p))
        bc = Bytecode()
        ast.eval(bc)

        bcs = [bc, one_more_bc]

        def f(arg):
            run(bcs[arg], print_fn)

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
