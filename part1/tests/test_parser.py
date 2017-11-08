
from interp.parser import parser
from interp.lexer import get_lexer
from interp import astnodes as ast

class TestParser(object):
    def parse(self, s):
        lexer = get_lexer()
        return parser.parse(lexer.lex(s))

    def test_parser_one(self):
        r = self.parse("""
            fun main() {
                return 3 + 2;
            }
            """)
        assert r == ast.Program([
            ast.Function('main', [],
                [
                ast.Return(ast.BinOp('+', ast.AstInteger(3), ast.AstInteger(2)))
                ])])

    def test_parse_if_while_expr(self):
        r = self.parse("""
            fun main() { 
               if 3 { 1; } 
               while x < 2 {
                  x = x + 2;
               }
            }
            """)
        exp = ast.Program([
            ast.Function('main', [], [
                ast.If(ast.AstInteger(3), [
                    ast.Discard(ast.AstInteger(1))
                ]),
                ast.While(ast.BinOp('<', ast.Atom('x'), ast.AstInteger(2)), [
                    ast.Assign('x', ast.BinOp('+', ast.Atom('x'), ast.AstInteger(2)))
                ])
            ])
        ])
        assert r == exp

    def test_parse_class_func_call(self):
        r = self.parse('''
            class X (a, b, c)
            fun main() {
                x = X(1, 2, 3);
            }

            fun f2(x) {
                x.x = (x.a + 3);
                x = X();
            }
            ''')
        exp = ast.Program([
            ast.Class('X', ['a', 'b', 'c']),
            ast.Function('main', [], [
                ast.Assign('x', ast.Call('X', [
                    ast.AstInteger(1), ast.AstInteger(2), ast.AstInteger(3)
                ]))
            ]),
            ast.Function('f2', ['x'], [
                ast.DottedAssign(ast.Atom('x'), 'x', ast.BinOp('+',
                    ast.DottedExpr(ast.Atom('x'), 'a'), ast.AstInteger(3))),
                ast.Assign('x', ast.Call('X', []))
            ])
        ])
        assert r == exp
