# coding=utf8
from lex import TOKEN
from tree import *
import sys, lex, yacc
import logging
import log

logger = logging.getLogger('stxt.inliner')

DEBUG = False

# Lexer
tokens = ['ESCAPESTRING', 
          'EMPHASIS', 
          'REFERENCE', 
          'SINGLESPECIALCHAR', 
          'CBLOCK' 
         ] 

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0: last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def t_ESCAPESTRING(t):
    r"(''(?P<s>[^*]+?)'')" # +?, non-greedy fashion
    m = t.lexer.lexmatch
    t.value = m.group('s')
    return t

def t_EMPHASIS(t):
    r'__(?P<t>[^*]+?)__'
    m = t.lexer.lexmatch
    t.value = Tree('emphasis', m.group('t'))
    return t

refpat =  r'\[\[('
refpat += r'(?P<l>[^|\]]+)\|(?P<a1>[^|\]]+)|' # [[label|address]] 
refpat += r'(?P<a2>[^|\]]+)'                  # [[address]]
refpat += r')]]'
@TOKEN(refpat)
def t_REFERENCE(t):
    m = t.lexer.lexmatch
    if m:
        if m.group('l'): # [[label|address]]
            t.value = ReferenceNode(m.group('a1'), m.group('l'))
        elif m.group('a2'): # [[address]]
            t.value = ReferenceNode(m.group('a2'))
    else: 
        logger.error("[%s]:It isn't correct address." % t.value)
        logger.error("error at %s:%s" % (t.lexer.sourcefile, t.lexer.lineno))
        sys.exit()

    t.value.file   = t.lexer.sourcefile
    t.value.lineno = t.lexer.lineno
    return t

#def t_EMAIL(t):
#    r'\b([\w._%+\-]+@[\w.\-]+\.[\w]{2,4})\b' 
#    t.value = Tree('email', t.value)
#    return t

def t_URL(t):
    r"\b(https?|ftp|gopher|telnet|file|notes|ms-help):(//)[\w\d:#%/;$()~_?\-=\\.&]*\b"
    t.value = Tree('url', t.value)
    return t

def t_SINGLESPECIALCHAR(t):
    r"['\[_]"
    return t

def t_CBLOCK(t):
    r"[^[_'\n]+"
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    c = t.value[0]
    raise lex.LexError('illegal char[%s](%s) at %s:%s:%s\n%s' % (c, 
                str(ord(t.value[0])), t.lexer.sourcefile, t.lexer.lineno, 
                find_column(t.lexer.lexdata, t), t.lexer.lexdata), 
                t.lexer.lexdata)

lexer = lex.lex(reflags=0)

# PARSER
def p_para(p):
    '''para : elem
            | para elem
    ''' 
    if len(p) == 2:
        p[0] = Tree('para', '')
        p[0].append(p[1])
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_elem(p):
    '''elem : cblock
            | element
    '''
    p[0] = p[1]

def p_element(p):
    '''element : REFERENCE
               | EMPHASIS
    '''
    p[0] = p[1]

def p_cblock(p):
    '''cblock : CBLOCK
              | SINGLESPECIALCHAR
              | ESCAPESTRING
              | cblock CBLOCK
              | cblock SINGLESPECIALCHAR
              | cblock ESCAPESTRING
    '''
    if len(p) == 2:
        p[0] = Tree('cblock', p[1])
    else:
        p[1].value += p[2]
        p[0] = p[1]

def p_error(p):
    console.error("inliner error report:")
    if p:
        console.error("error at %s:%s" % (p.lexer.sourcefile, 
                                          p.lexer.lineno))
        console.error("Input %s" % p.type)
    sys.exit()

parser = yacc.yacc()

def parse(input, source='__string__', slineno=1):
    #import pdb
    #pdb.set_trace()
    if len(input) == 0:
        msg  ='Inliner.WARN:: %s:%s is empty.' % (source, slineno),
        raise AttributeError, msg

    if slineno is not None:
        lexer.lineno = slineno + 1
    else:
        raise AttributeError, 'inliner.parse, slineno is None!'

    lexer.sourcefile = source
    d = parser.parse(input, lexer=lexer, tracking=True, debug=DEBUG)
    d.value = input
    return d
