
from interp.lexer import get_lexer

class TestLexer(object):
    def lex(self, s):
        return [x.name for x in get_lexer().lex(s)]

    def test_lexer(self):
        assert self.lex("a + b;") == ['IDENTIFIER', 'PLUS', 'IDENTIFIER',
                                      'SEMICOLON']
