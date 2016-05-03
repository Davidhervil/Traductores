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
'TkRotacion','TkTrasposicion''TkNum','TkBegin','TkID','TkTrue','TkFalse',\
'TkCaracter','TkWhile','TkIf','TkWith','TkVar','TkEnd','TkInt','TkChar',\
'TkBool','TkOf','TkMatrix','TkOtherwise','TkFor','TkFrom','TkTo','TkStep',\
'TkRead','TkPrint','TkNot')

# Regular expression rules for simple tokens
t_TkComa = r','
t_TkPunto = r'\.'
t_TkDosPuntos = r'\:'
t_TkParAbre = r'\('
t_TkParCierra = r'\)'
t_TkCorcheteAbre = r'\['
t_TkCorcheteCierra = r'\]'
t_TkLlaveAbre = r'\{'
t_TkLLaveCierra = r'\}'
t_TkHacer = r'hacer'
t_TkAsignacion = r'\<-'
t_TkSuma = r'\+'
t_TkResta = r'-'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'\%'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

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

