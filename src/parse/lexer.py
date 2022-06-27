import ply.lex as lex

tokens = ('WORD', 'AND', 'NOT', 'OR')

def t_AND(t):
    r'~AND~'
    return t

def t_NOT(t):
    r'~NOT~'
    return t

def t_OR(t):
    r'~OR~'
    return t

def t_WORD(t):
    r'[a-z0-9,./;\'\[\]<>?:"&~|{}`!@#$%^*()_+=-]+'
    return t

def t_error(t):
    t.lexer.skip(1)

t_ignore = '  \t\f\r\t\v'

lexer = lex.lex()