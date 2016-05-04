# ------------------------------------------------------------
# calclex.py
#
# RECOMENDACION VER EJEMPLO DE >>>>>>> http://www.dabeaz.com/ply/example.html
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

import ply.lex as lex

# List of token names.   This is always required
tokens = ('TkComa','TkPunto','TkDosPuntos','TkParAbre','TkParCierra',\
'TkCorcheteAbre','TkCorcheteCierra','TkLlaveAbre','TkLlaveCierra','TkHacer'\
,'TkAsignacion','TkSuma','TkResta','TkMult','TkDiv','TkMod','TkConjuncion',\
'TkDisyuncion','TkNegacion','TkMenor','TkMenorIgual','TkMayor','TkMayorIgual'\
,'TkIgual','TkSiguienteCar','TkAnteriorCar','TkValorAscii','TkConcatenacion',\
'TkRotacion','TkTrasposicion','TkNum','TkBegin','TkId','TkTrue','TkFalse',\
'TkCaracter','TkWhile','TkIf','TkWith','TkVar','TkEnd','TkInt','TkChar',\
'TkBool','TkOf','TkMatrix','TkOtherwise','TkFor','TkFrom','TkTo','TkStep',\
'TkRead','TkPrint')

reservados = {'not':'TkNegacion','begin':'TkBegin','with':'TkWith'}


# Regular expression rules for simple tokens
t_TkComa = r','
t_TkPunto = r'\.'
t_TkDosPuntos = r'\:'
t_TkParAbre = r'\('
t_TkParCierra = r'\)'
t_TkCorcheteAbre = r'\['
t_TkCorcheteCierra = r'\]'
t_TkLlaveAbre = r'\{'
t_TkLlaveCierra = r'\}'
t_TkHacer = r'-\>'
t_TkAsignacion = r'\<-'
t_TkSuma = r'\+'
t_TkResta = r'-'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'\%'
t_TkConjuncion = r'/\\'
t_TkDisyuncion = r'\\/'
t_TkMenor = r'\<'
t_TkMenorIgual = r'\<='
t_TkMayor = r'\>'
t_TkMayorIgual = r'\>='
t_TkIgual = r'='
t_TkSiguienteCar = r'\+\+'
t_TkAnteriorCar = r'--'
t_TkValorAscii = r'\#'
t_TkConcatenacion = '\:\:'
t_TkRotacion = r'\$'
t_TkTrasposicion = r'\?'
t_TkNum = r'\d+'  ####################chequear funcion
t_TkCaracter = r'\'(.|\\\w)\''
# A regular expression rule with some action code
# Define a rule so we can track line numbers

def t_TkBegin(t):
    r'begin$'
    t.type = reservados.get(t.value,'TkBegin')
    return t 

def t_TkWith(t):
    r'with$'
    t.type = reservados.get(t.value,'TkWith')
    return t 

def t_TkId(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	t.type = reservados.get(t.value,'TkId')
	return t

def t_TkNegacion(t):
    r'not$'
    t.type = reservados.get(t.value,'TkNegacion')
    return t

def t_TkTrue(t):
    r'True$'
    t.type = reservados.get(t.value,'TkTrue')
    return t 

def t_TkFalse(t):
    r'False$'
    t.type = reservados.get(t.value,'TkFalse')
    return t 

def t_TkWhile(t):
    r'while$'
    t.type = reservados.get(t.value,'TkWhile')
    return t 
def t_TkIf(t):
    r'if$'
    t.type = reservados.get(t.value,'TkIf')
    return t 

def t_TkVar(t):
    r'var$'
    t.type = reservados.get(t.value,'TkVar')
    return t 
def t_TkEnd(t):
    r'end$'
    t.type = reservados.get(t.value,'TkEnd')
    return t 

def t_TkInt(t):
    r'int$'
    t.type = reservados.get(t.value,'TkInt')
    return t

def t_TkChar(t):
    r'char$'
    t.type = reservados.get(t.value,'TkChar')
    return t 

def t_TkBool(t):
    r'bool$'
    t.type = reservados.get(t.value,'TkBool')
    return t  

def t_TkOf(t):
    r'of$'
    t.type = reservados.get(t.value,'TkOf')
    return t 

def t_TkMatrix(t):
    r'matrix$'
    t.type = reservados.get(t.value,'TkMatrix')
    return t

def t_TkOtherwise(t):
    r'otherwise$'
    t.type = reservados.get(t.value,'TkOtherwise')
    return t 

def t_TkFor(t):
    r'for$'
    t.type = reservados.get(t.value,'TkFor')
    return t 

def t_TkFrom(t):
    r'from$'
    t.type = reservados.get(t.value,'TkFrom')
    return t 

def t_TkTo(t):
    r'to$'
    t.type = reservados.get(t.value,'TkTo')
    return t 

def t_TkStep(t):
    r'step$'
    t.type = reservados.get(t.value,'TkStep')
    return t 

def t_TkRead(t):
    r'read$'
    t.type = reservados.get(t.value,'TkRead')
    return t 

def t_TkPrint(t):
    r'print$'
    t.type = reservados.get(t.value,'TkPrint')
    return t 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# A string containing ignored characters (spaces and tabs)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
t_ignore  = ' \t'

content = '''
begin23 begin beginbegin with begin\n
3 + 4 * 10
  + -20 *2
'''
lexer = lex.lex()
lexer.input(content)
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)


