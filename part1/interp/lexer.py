from rply.lexergenerator import LexerGenerator
from rply.token import Token as RplyToken


class Token(RplyToken):
    def getsrcpos(self):
        return (self.source_pos.start, self.source_pos.end)


class SourceRange(object):
    def __init__(self, start, end, lineno, colno):
        self.start = start
        self.end = end
        self.lineno = lineno
        self.colno = colno

    def __repr__(self):
        return "SourceRange(start=%d, end=%d, lineno=%d, colno=%d)" % (
            self.start, self.end, self.lineno, self.colno)


class ParseError(Exception):
    def __init__(self, msg, line, filename, lineno, start_colno, end_colno):
        self.msg = msg
        self.line = line
        self.filename = filename
        self.lineno = lineno
        self.start_colno = start_colno
        self.end_colno = end_colno

    def __str__(self):
        # 6 comes from formatting of ParseError by pytest
        return (self.line + "\n" + " " * (self.start_colno - 6) +
                "^" * (self.end_colno - self.start_colno))


RULES = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('DIV', r'/'),
    ('LE', r'\<='),
    ('GE', r'\>='),
    ('LT', r'\<'),
    ('GT', r'\>'),
    ('STAR', r'\*'),
    ('DOT', r'\.'),
    ('EQ', r'=='),
    ('NE', r'!='),
    ('ASSIGN', r'='),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LEFT_BRACE', r'\{'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('RIGHT_BRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';')
]

KEYWORDS = [
    'fun',
    'class',
    'return',
    'while',
    'if',
]

TOKENS = [x[0] for x in RULES] + [x.upper() for x in KEYWORDS]

KEYWORD_DICT = dict.fromkeys(KEYWORDS)

def get_lexer():
    lg = LexerGenerator()
    lg.ignore("\s+")
    for keyword in KEYWORDS:
        lg.add(keyword.upper(), keyword)
    for token, r in RULES:
        lg.add(token, r)
    return lg.build()
