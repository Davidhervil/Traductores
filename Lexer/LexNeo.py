# ------------------------------------------------------------
# calclex.py
#
# RECOMENDACION VER EJEMPLO DE >>>>>>> http://www.dabeaz.com/ply/example.html
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
from __future__ import print_function
import ply.lex as lex
COLUMNA = [0,1,0]
# List of token names.   This is always required
tokens = ('TkComa','TkPunto','TkDosPuntos','TkParAbre','TkParCierra',\
'TkCorcheteAbre','TkCorcheteCierra','TkLlaveAbre','TkLlaveCierra','TkHacer'\
,'TkAsignacion','TkSuma','TkResta','TkMult','TkDiv','TkMod','TkConjuncion',\
'TkDisyuncion','TkNegacion','TkMenor','TkMenorIgual','TkMayor','TkMayorIgual'\
,'TkIgual','TkSiguienteCar','TkAnteriorCar','TkValorAscii','TkConcatenacion',\
'TkRotacion','TkTrasposicion','TkNum','TkBegin','TkId','TkTrue','TkFalse',\
'TkCaracter','TkWhile','TkIf','TkWith','TkVar','TkEnd','TkInt','TkChar',\
'TkBool','TkOf','TkMatrix','TkOtherwise','TkFor','TkFrom','TkTo','TkStep',\
'TkRead','TkPrint','TkComenAbre','TkComenCierra','TkError')

reservados = {'not':'TkNegacion','begin':'TkBegin','with':'TkWith','True':'TkTrue',\
'False':'TkFalse','while':'TkWhile','if':'TkIf','var':'TkVar','end':'TkEnd','int':'TkInt',\
'char':'TkChar','bool':'TkBool','of':'TkOf','matrix':'TkMatrix','otherwise':'TkOtherwise',\
'for':'TkFor','from':'TkFrom','to':'TkTo','step':'TkStep','print':'TkPrint','read':'TkRead'}
    

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
t_TkComenAbre = r'\%\{'
t_TkComenCierra = r'\}\%'
t_ignore_linea = r'\%\%[^\n.]*'
# A regular expression rule with some action code
# Define a rule so we can track line numbers

def t_TkId(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reservados.get(t.value,'TkId')
    return t

def t_TkBegin(t):
    r'begin\Z'
    t.type = reservados.get(t.value,'TkBegin')
    return t 

def t_TkWith(t):
    r'with\Z'
    t.type = reservados.get(t.value,'TkWith')
    return t 

def t_TkNegacion(t):
    r'not\Z'
    t.type = reservados.get(t.value,'TkNegacion')
    return t

def t_TkTrue(t):
    r'True\Z'
    t.type = reservados.get(t.value,'TkTrue')
    return t 

def t_TkFalse(t):
    r'False\Z'
    t.type = reservados.get(t.value,'TkFalse')
    return t 

def t_TkWhile(t):
    r'while\Z'
    t.type = reservados.get(t.value,'TkWhile')
    return t 
def t_TkIf(t):
    r'if\Z'
    t.type = reservados.get(t.value,'TkIf')
    return t 

def t_TkVar(t):
    r'var\Z'
    t.type = reservados.get(t.value,'TkVar')
    return t 
def t_TkEnd(t):
    r'end\Z'
    t.type = reservados.get(t.value,'TkEnd')
    return t 

def t_TkInt(t):
    r'int\Z'
    t.type = reservados.get(t.value,'TkInt')
    return t

def t_TkChar(t):
    r'char\Z'
    t.type = reservados.get(t.value,'TkChar')
    return t 

def t_TkBool(t):
    r'bool\Z'
    t.type = reservados.get(t.value,'TkBool')
    return t  

def t_TkOf(t):
    r'of\Z'
    t.type = reservados.get(t.value,'TkOf')
    return t 

def t_TkMatrix(t):
    r'matrix\Z'
    t.type = reservados.get(t.value,'TkMatrix')
    return t

def t_TkOtherwise(t):
    r'otherwise\Z'
    t.type = reservados.get(t.value,'TkOtherwise')
    return t 

def t_TkFor(t):
    r'for\Z'
    t.type = reservados.get(t.value,'TkFor')
    return t 

def t_TkFrom(t):
    r'from\Z'
    t.type = reservados.get(t.value,'TkFrom')
    return t 

def t_TkTo(t):
    r'to\Z'
    t.type = reservados.get(t.value,'TkTo')
    return t 

def t_TkStep(t):
    r'step\Z'
    t.type = reservados.get(t.value,'TkStep')
    return t 

def t_TkRead(t):
    r'read\Z'
    t.type = reservados.get(t.value,'TkRead')
    return t 

def t_TkPrint(t):
    r'print\Z'
    t.type = reservados.get(t.value,'TkPrint')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    COLUMNA[0]=0
    COLUMNA[1] = 1
# A string containing ignored characters (spaces and tabs)

# Error handling rule
def t_error(t):
    if(COLUMNA[2]==0):
        print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
#def t_ignore_comentariolinea(t):
#    r'\%\%[^\n.]*'


def t_tab(t):
    r'\t+'
    #COLUMNA[0] = (COLUMNA[0] // 4)*4 + 1*(COLUMNA[0]%4==3) + 2*(COLUMNA[0]%4==2) + 3*(COLUMNA[0]%4==1) -1*(COLUMNA[0]%4!=0) 
    COLUMNA[0] = (4-(((t.lexpos + COLUMNA[0]) )%4))*len(t.value)-(len(t.value)-1)
    COLUMNA[1] = 0
def t_espacio(t):
    r'\s'
    COLUMNA[1] = 0

contenido = '''
begin23 begin beginbegin with begin\n
var huehuehue
3 + 4 * 10
  + -20 *2
'''
f = open("flojera.txt",'r')
#contenido = f.read()
lexer = lex.lex()
#lexer.input(contenido)

while True:
    COLUMNA[2] = 0
    for lines in f.readlines():
        boole=True
        lexer.input(lines)
        while True:
            tok = lexer.token()
            if not tok:
                if(boole==False):
                    print('')
                break      # No more input
            if(tok.type=="TkComenAbre"):
                COLUMNA[2]=1
            elif(tok.type=="TkComenCierra"):
                COLUMNA[2]=0
            elif(COLUMNA[2]==0):
                if(tok.type=="TkId"):
                    print(str(tok.type) +"(\"" +tok.value+ "\") "+str(tok.lineno)+" "+ str(tok.lexpos+COLUMNA[0]+COLUMNA[1])+", ",end="")
                    boole=False
                elif(tok.type=="TkNum"):
                    boole=False
                    print(str(tok.type) +"(" +tok.value+ ") "+str(tok.lineno)+" "+ str(tok.lexpos+COLUMNA[0]+COLUMNA[1])+", ",end="")
                elif tok.type != "tab" and tok.type != "espacio":
                    boole=False
                    print(str(tok.type) +" "+ str(tok.lineno)+" "+str(tok.lexpos+COLUMNA[0]+COLUMNA[1])+", ",end="")
    break
