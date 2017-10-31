
from rply import ParserGenerator
from interp.lexer import TOKENS
from interp import astnodes as ast

pg = ParserGenerator(TOKENS, precedence=
    [
        ('left', ['EQ', 'LT', 'GT', 'NE', 'LE', 'GE']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['DIV', 'STAR']),
        ('left', ['DOT']),
        ('left', ['LEFT_PAREN']),
    ])

@pg.production('main : program')
def main(p):
    return ast.Program(p[0].get_elem_list())

@pg.production('program : ')
@pg.production('program : program_element program')
def program(p):
    if len(p) == 0:
        return ast.StatementList(None, None)
    return ast.StatementList(p[0], p[1])

@pg.production('program_element : function')
@pg.production('program_element : class')
def program_element(p):
    return p[0]

@pg.production('function : FUN IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN LEFT_BRACE '
               'statement_list RIGHT_BRACE')
def function(p):
    return ast.Function(p[1].getstr(), p[3].get_arg_list(), p[6].get_elem_list())

@pg.production('class : CLASS IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN')
def class_(p):
    return ast.Class(p[1].getstr(), p[3].get_arg_list())

@pg.production('statement_list : ')
@pg.production('statement_list : statement statement_list')
def statement(p):
    if len(p) == 0:
        return ast.StatementList(None, None)
    return ast.StatementList(p[0], p[1])

@pg.production('argument_list : ')
@pg.production('argument_list : argument_rest')
def argument_list(p):
    if len(p) == 0:
        return ast.ArgumentList(None, None)
    return p[0]

@pg.production('argument_rest : IDENTIFIER')
@pg.production('argument_rest : IDENTIFIER COMMA argument_rest')
def argument_rest(p):
    if len(p) == 1:
        nxt = ast.ArgumentList(None, None) # sentinel
    else:
        nxt = p[2]
    return ast.ArgumentList(p[0].getstr(), nxt)

@pg.production('statement : expression SEMICOLON')
def statement_expression(p):
    return ast.Discard(p[0])

@pg.production('statement : RETURN expression SEMICOLON')
def statement_return(p):
    return ast.Return(p[1])

@pg.production('statement : IDENTIFIER ASSIGN expression SEMICOLON')
@pg.production('statement : atom DOT IDENTIFIER ASSIGN expression SEMICOLON')
def statement_assign(p):
    if len(p) == 4:
        return ast.Assign(p[0].getstr(), p[2])
    return ast.DottedAssign(p[0], p[2].getstr(), p[4])

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression STAR expression')
@pg.production('expression : expression DIV expression')
@pg.production('expression : expression EQ expression')
@pg.production('expression : expression NE expression')
@pg.production('expression : expression LE expression')
@pg.production('expression : expression GE expression')
@pg.production('expression : expression LT expression')
@pg.production('expression : expression GT expression')
def expression_binop(p):
    return ast.BinOp(p[1].getstr(), p[0], p[2])

@pg.production('expression : INTEGER')
def expression_integer(p):
    return ast.Integer(int(p[0].getstr()))

@pg.production('expression : atom')
def expression_identifier(p):
    return p[0]

@pg.production('atom : IDENTIFIER')
@pg.production('atom : atom DOT IDENTIFIER')
def atom(p):
    if len(p) == 1:
        return ast.Atom(p[0].getstr())
    return ast.DottedExpr(p[0], p[2].getstr())

@pg.production('expression : LEFT_PAREN expression RIGHT_PAREN')
def expression_paren(p):
    return p[1]

@pg.production('atom : IDENTIFIER LEFT_PAREN expression_list RIGHT_PAREN')
def expression_func_call(p):
    return ast.Call(p[0].getstr(), p[2].get_elem_list())

@pg.production('expression_list : ')
@pg.production('expression_list : non_empty_expr_list')
def expression_list(p):
    if len(p) == 0:
        return ast.StatementList(None, None)
    return p[0]

@pg.production('non_empty_expr_list : expression')
@pg.production('non_empty_expr_list : expression COMMA non_empty_expr_list')
def non_empty_expr_list(p):
    if len(p) == 1:
        nxt = ast.StatementList(None, None)
    else:
        nxt = p[2]
    return ast.StatementList(p[0], nxt)

@pg.production('statement : IF expression LEFT_BRACE statement_list RIGHT_BRACE')
def statement_if(p):
    return ast.If(p[1], p[3].get_elem_list())

@pg.production('statement : WHILE expression LEFT_BRACE statement_list RIGHT_BRACE')
def statement_while(p):
    return ast.While(p[1], p[3].get_elem_list())

parser = pg.build()
