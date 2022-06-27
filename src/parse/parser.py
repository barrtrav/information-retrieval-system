import ply.yacc as yacc
from .lexer import tokens

def p_p(p):
    '''p : t x'''
    
    p[0] = ' ( ' + p[1] + ' ) ' + p[2]

def p_x(p):
    '''x : OR t x
         | '''
    try: p[0] = ' OR ' + ' ( ' + p[2] + ' ) ' + p[3]
    except IndexError: p[0] = ''

def p_t(p):
    '''t : f y'''
    
    p[0] = p[1] + p[2]


def p_y(p):
    '''y : AND f y
         |'''
    
    try: p[0] = ' AND ' + p[2] + p[3]
    except IndexError: p[0] = ''
    
def p_f(p):
    '''f : NOT f
         | WORD f
         | WORD'''
    
    try:
        if p[1] == '~NOT~': p[0] =  f'NOT ( {p[2]} )'
        else:p[0] =  p[1] + ' ' + p[2]
    except IndexError: 
        p[0] = p[1]
    

def p_error(p):
    pass

parse = yacc.yacc(start='p')