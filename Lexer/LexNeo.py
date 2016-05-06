# ------------------------------------------------------------
# LexNeo.py
#
# Autores:
#   Arturo Toro
#   David Hernandez
# ------------------------------------------------------------
from __future__ import print_function
import ply.lex as lex
import sys
CORRECCION = [0,1,0,0]  #Variable auxiliar cuyas posiciones permiten ajustar el filtrado de contenido
                        #    Posiciones:
                        #       0 Cantidad de espacios a correr debido a las tabulaciones
                        #       1 Espacio individual a sumar
                        #       2 Booleano auxiliar que permite saber si se esta dentro de un comentario
                        #       3 Booleano auxiliar que permite saber si se detecto error en una linea

apertura = [-1,-1]      #Variable auxiliar para guardar la posicion de la ultima apertura de
                        #   comentario sin cerrar
ajuste = [0,0]          #Variable auxiliar que permite guarar el ajuste por tabulaciones y espacios
                        #   necesario para la ultima apertura de comentario sin cerrar
# Lista de nombres de tokens.
tokens = ('TkComa','TkPunto','TkDosPuntos','TkParAbre','TkParCierra',\
'TkCorcheteAbre','TkCorcheteCierra','TkLlaveAbre','TkLlaveCierra','TkHacer'\
,'TkAsignacion','TkSuma','TkResta','TkMult','TkDiv','TkMod','TkConjuncion',\
'TkDisyuncion','TkNegacion','TkMenor','TkMenorIgual','TkMayor','TkMayorIgual'\
,'TkIgual','TkSiguienteCar','TkAnteriorCar','TkValorAscii','TkConcatenacion',\
'TkRotacion','TkTrasposicion','TkNum','TkBegin','TkId','TkTrue','TkFalse',\
'TkCaracter','TkWhile','TkIf','TkWith','TkVar','TkEnd','TkInt','TkChar',\
'TkBool','TkOf','TkMatrix','TkOtherwise','TkFor','TkFrom','TkTo','TkStep',\
'TkRead','TkPrint','TkComenAbre','TkComenCierra','TkError')

#Lista de palabras reservadas
reservados = {'not':'TkNegacion','begin':'TkBegin','with':'TkWith','True':'TkTrue',\
'False':'TkFalse','while':'TkWhile','if':'TkIf','var':'TkVar','end':'TkEnd','int':'TkInt',\
'char':'TkChar','bool':'TkBool','of':'TkOf','matrix':'TkMatrix','otherwise':'TkOtherwise',\
'for':'TkFor','from':'TkFrom','to':'TkTo','step':'TkStep','print':'TkPrint','read':'TkRead'}
    

# Expresiones regulares para tokens simples
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
t_TkNum = r'\d+'  
t_TkCaracter = r'\'(.|\\[a-zA-Z])\''
t_TkComenAbre = r'\%\{'
t_TkComenCierra = r'\}\%'
t_ignore_linea = r'\%\%[^\n.]*'

#Expresiones regulares que tienen asociados un metodo

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

#
def t_newline(t):
    #   Al ver un salto de linea incrementamos la cantidad de lineas y reiniciamos las tabulaciones
    #   y espacios. Los espacios los colocamos en 1 puesto que el contador de columnas de PLY inicia en 0
    r'\n+'
    t.lexer.lineno += len(t.value)
    CORRECCION[0]=0
    CORRECCION[1] = 1

#   Manejo de Errores
def t_error(t):
    if(CORRECCION[2]==0):
        print("Error: Caracter inesperado '"+ str(t.value[0])+\
            "' en la fila "+str(t.lineno+CORRECCION[0]+CORRECCION[1])+\
            ", columna "+str(t.lexpos+CORRECCION[0]+CORRECCION[1]))
    CORRECCION[3]=1
    t.lexer.skip(1)

# Build the lexer

def t_tab(t):
    # Cuando vemos un tabulador o mas, procuramos desplazar el numero de columnas al multiplo
    #   mas 1 de 4 siguiente a la posicion actual acumulando este calculo segun la cantidad
    #   de tabulaciones.
    # El ajuste de tabulaciones hace necesario tener que reiniciar la posicion de espacios
    #   de CORRECCION en 0 si no se ha leido tabulador, o dejarlo en 1 si no se ha leido alguno  
    r'\t+'
    CORRECCION[0] = (4-(((t.lexpos + CORRECCION[0]) )%4))*len(t.value)-(len(t.value)-1)
    CORRECCION[1] = 0
def t_espacio(t):
    r'\s'
    if CORRECCION[0]==0:
        CORRECCION[1] = 1
    else:    
        CORRECCION[1] = 0

try:
    f = open(sys.argv[1],'r')
except:
    print("No se pudo abrir el archivo")
    exit(0)
#Construccion del lexer
lexer = lex.lex()

while True:
    CORRECCION[2] = 0
    for lines in f.readlines():
        boole=True
        salida=""
        CORRECCION[3]=0
        lexer.input(lines)
        while True:
            tok = lexer.token()
            if not tok:
                if(boole==False):
                    if(CORRECCION[3]!=1):
                        salida[len(salida)-2]
                        print(salida,end="")
                        print('')
                break      # No more input
            if(tok.type=="TkComenAbre"):
                if(CORRECCION[2]==0):
                    apertura[0] = tok.lineno
                    apertura[1] = tok.lexpos
                    ajuste[0] = CORRECCION[0]
                    ajuste[1] = CORRECCION[1]
                CORRECCION[2]=1
            elif(tok.type=="TkComenCierra"):
                CORRECCION[2]=0
            elif(CORRECCION[2]==0):
                if((tok.type=="TkId")):
                    salida+=(str(tok.type) +"(\"" +tok.value+ "\") "+str(tok.lineno)+" "+ str(tok.lexpos+CORRECCION[0]+CORRECCION[1])+", ")
                    boole=False
                elif((tok.type=="TkNum")| (tok.type=="TkCaracter")):
                    boole=False
                    salida+=(str(tok.type) +"(" +tok.value+ ") "+str(tok.lineno)+" "+ str(tok.lexpos+CORRECCION[0]+CORRECCION[1])+", ")
                elif tok.type != "tab" and tok.type != "espacio":
                    boole=False
                    salida+=(str(tok.type) +" "+ str(tok.lineno)+" "+str(tok.lexpos+CORRECCION[0]+CORRECCION[1])+", ")
    break
if(CORRECCION[2]==1):
    print("Error: EOF "+str(apertura[0])+" "+str(apertura[1]+ajuste[0]+ajuste[1]))
