
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

    def test_if(self):
        p = self.interp("""
        fun main() {
            if 2+1 == 3 {
              print(1);
              print(2);
            }
        }
        """)
        assert p[0].intval == 1
        assert p[1].intval == 2

    def test_while(self):
        p = self.interp("""
        fun main() {
            i = 2;
            while i < 5 {
                print(i);
                i = i + 1;
            }
        }
        """)
        assert p[0].intval == 2
        assert p[1].intval == 3
        assert p[2].intval == 4

    def test_call(self):
        p = self.interp("""
        fun main() {
            foo(5,4);
            bar(3,2,1);
            print(0);
        }
        fun foo(a, b) {
            print(a);
            print(b);
        }
        fun bar(x, y, z) {
            print(x);
            print(y);
            print(z);
        }
        """)
        assert p[0].intval == 5
        assert p[1].intval == 4
        assert p[2].intval == 3
        assert p[3].intval == 2
        assert p[4].intval == 1
        assert p[5].intval == 0

    def test_return(self):
        p = self.interp("""
        fun main() {
            t = foo(1,2,3);
            print(t);
        }
        fun foo(a, b, c) {
            return a + b + c;
        }
        """)
        assert p[0].intval == 6

    def test_getattr(self):
        p = self.interp("""
        class foo (a,b,c)
        fun main() {
            obj = foo(1, 2, 3);
            print(obj.c);
            print(obj.b);
            print(obj.a);
        }
        """)
        assert p[0].intval == 3
        assert p[1].intval == 2
        assert p[2].intval == 1

    def test_setattr(self):
        p = self.interp("""
        class foo (a, b, c)
        fun main() {
            obj = foo(1, 2, 3);
            obj.b = 5;
            print(obj.a);
            print(obj.b);
            print(obj.c);
        }
        """)
        assert p[0].intval == 1
        assert p[1].intval == 5
        assert p[2].intval == 3

    def test_return_if(self):
        p = self.interp("""
        fun main() {
            print(foo(1));
            print(foo(2));
            print(foo(3));
            print(foo(4));
        }
        fun foo(t) {
            if t == 1 {
                return 10;
            }
            if t == 2 {
                return 20;
            }
            if t == 3 {
                return 30;
            }
            return 40;
        }
        """)
        assert p[0].intval == 10
        assert p[1].intval == 20
        assert p[2].intval == 30
        assert p[3].intval == 40
