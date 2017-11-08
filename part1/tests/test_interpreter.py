
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

    def test_addition(self):
        p = self.interp("""
        fun main() {
            print(1 + 2);
        }
        """)
        assert p[0].intval == 3
        
    def test_variable(self):
        p = self.interp("""
        fun main() {
            a = 2;
            print(a);
        }
        """)
        assert p[0].intval == 2

    def test_while(self):
        p = self.interp("""
        fun main() {
            i = 0;
            while i < 10 {
                i = i + 1;
            }
            print(i);
        }
        """)
        assert p[0].intval == 10

    def test_function_call(self):
        p = self.interp("""
        fun f() {
            return 3;
        }
        fun main() {
            print(f());
        }
        """)
        assert p[0].intval == 3

    def test_arguments_pass(self):
        p = self.interp("""
        fun f(a, b) {
            return a + b;
        }
        fun main() {
            print(f(1, 2));
        }
        """)        
        assert p[0].intval == 3

    def test_object_creation(self):
        p = self.interp("""
        class X(a, b, c)

        fun main() {
            x = X(1, 2, 3);
            print(x.b);
            print(x.a);
            print(x.c);
        }
        """)
        assert p[0].intval == 2
        assert p[1].intval == 1
        assert p[2].intval == 3

    def test_setitem(self):
        p = self.interp("""
        class X(a, b, c)

        fun main() {
            x = X(1, 2, 3);
            x.xyz = 13;
            print(x.xyz);
        }
        """)
        assert p[0].intval == 13
