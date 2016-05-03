# ------------------------------------------------------------
# calclex.py
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
t_TkHacer = r'hacer'
t_TkAsignacion = r'\<-'
t_TkSuma = r'\+'
t_TkResta = r'-'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'\%'
t_TkConjuncion = r'/\\'
t_TkDisyuncion = r'\\/'
t_TkNegacion = r'not'
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
t_TkBegin = r'begin'
t_TkId = r'[a-zA-Z][a-zA-Z0-9_]*'
t_TkTrue = r'True'
t_TkFalse = r'False'
t_TkCaracter = r'\'[a-zA-Z]\''




# A regular expression rule with some action code
#def t_NUMBER(t):
#    r'\d+'
#    t.value = int(t.value)    
#    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
import ply.lex as lex
# Build the lexer
lexer = lex.lex()
f = open('flojera.txt','r')
content= f.read()
lexer.input(content)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

