from LexNeo import tokens,reservados,lexy
from GramNeo import *
import ply.yacc as yacc
import sys
precedence = (
    ('nonassoc','TkIgual','TkDesigual','TkMayor','TkMenor','TkMayorIgual','TkMenorIgual'),
    ('left', 'TkSuma', 'TkResta','TkConcatenacion', 'TkDisyuncion'),
    ('left', 'TkMult', 'TkDiv','TkConjuncion','TkRotacion'),
    ('left','TkMod','TkSiguienteCar','TkAnteriorCar'),
    ('right', 'UTkResta','TkNegacion','TkTrasposicion',), 
    ('nonassoc','TkValorAscii')           # Unary minus operator
)
global tablaSimb    # Variable global empleada para construir las tablas durante la ejecucion del parser.
tablaSimb = dict()  # Es un diccionario cuya clave es el nombre de la variable y el valor es el tipo.

def p_NEO(p):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
           | TkBegin INSTGEN TkEnd''' 

    global tablaSimb
    if p[1] == 'with':
        p[0] = cNeo(p[2],p[4],tablaSimb.copy())
        p[0].tabla = p[2].tabla
    else:
        p[0] = cNeo(None,p[2],tablaSimb.copy())
    tablaSimb.clear()

def p_empty(p):
    '''empty :'''
    pass

def p_LIST_DEC(p):
    '''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
                | LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''
    global tablaSimb
    if p[1] == 'var':
        p[0] = cList_Dec(None,p[2],p[4],tablaSimb.copy())                # Nodo Parser                            
        for ident in p[2].lista:                        # Obtenemos la lista de identificadores
            if not p[0].tabla.__contains__(ident[0]):   # Si el elemento no esta, entonces verificamos el tipo
                if ident[1]==p[4] or ident[1]=="":                      # Si el tipo es el correcto, entonces lo agregamos a la tabla
                    p[0].tabla[ident[0]] = p[4]         # Agregamos el elemento a la tabla con el tipo correspondiente.
                else:
                    print("Error de tipo: "+str(ident[0])+" de tipo "+str(p[4])+" pero se le asigno "+str(ident[1]))
                    exit(0)
            else:
                print("La variable "+str(ident[0])+" fue declarada anteriormente")
                exit(0)
    else:  
        p[0] = cList_Dec(p[1],p[3],p[5],tablaSimb.copy())  # Nodo Parser
        p[0].tabla = p[1].tabla
        for ident in p[3].lista:                        # Obtenemos la lista de identificadores
            if not p[0].tabla.__contains__(ident[0]):   # Si el elemento no esta, entonces verificamos el tipo
                if ident[1]==p[5] or ident[1]=="":      # Si el tipo es el correcto, entonces lo agregamos a la tabla
                    p[0].tabla[ident[0]] = p[5]         # Agregamos el elemento a la tabla con el tipo correspondiente.
                else:
                    print("Error de tipo: "+str(ident[0])+" de tipo "+str(p[5])+" pero se le asigno "+str(ident[1]))
                    exit(0)
            else:
                print("La variable "+str(ident[0])+" fue declarada anteriormente")
                exit(0)
    
    #tablaSimb = p[0].tabla.copy()
def p_TIPO(p):
    '''TIPO : TkInt
            | TkBool
            | TkChar
            | TkMatrix TkCorcheteAbre DIM TkCorcheteCierra TkOf TIPO'''
    global tablaSimb
    if len(p) == 2:
        p[0] = p[1]                         # QUIZAS HAGA FALTA HACERLO CLASE TAMBIEN (COMO EN EXPRESION)
    else:
        p[0] = cMatriz(p[3],p[6],tablaSimb )
        if isinstance(p[3],cDim):
            p[0].numDim = p[3].numDim
            p[0].card_dim = p[3].card_dim
        else:
            p[0].numDim = 1
            p[0].card_dim = 1

        if isinstance(p[6],cMatriz):
            p[0].numDim += p[6].numDim
            p[0].tipobase = p[6].tipobase
        else:
            p[0].tipobase = p[6]

def p_DIM(p):
    '''DIM  : EXPR
            | DIM TkComa EXPR'''
    if len(p) == 2:
        p[0] = p[1] #Esto es correcto ? porque pareciera que no tuviera Dim. Ademas, monascal dijo que hay que veriicar numero de dimensiones
        #si tenemos un arreglo de dimensiones eso se facilita mucho
    else:
        p[0] = cDim(p[1],p[3])
        if isinstance(p[1],cDim):
            p[0].numDim = 1 + p[1].numDim
            p[0].card_dim = 1 + p[1].card_dim
        else:
            p[0].numDim = 2
            p[0].card_dim = 2

def p_LIST_IDEN(p):
    '''LIST_IDEN : TkId OPASIG
                 | LIST_IDEN TkComa TkId OPASIG'''
    global tablaSimb
    if len(p) == 3:
        p[0] = cList_Iden(None,p[2],p[1],tablaSimb,len(p))               # Nodo parser
        p[0].lista = [(p[1],"")]
    else:
        p[0] = cList_Iden(p[1],p[4],p[3],tablaSimb,len(p))               # Nodo Parser :D
        p[0].lista = p[1].lista + [(p[3],"")]

def p_OPASIG(p):
    '''OPASIG : TkAsignacion EXPR
              | empty'''
    global tablaSimb
    if len(p) == 3:
        p[0] = cOpasig(p[2],tablaSimb)
    else:
        p[0] = ""

def p_INST(p):
    '''INST : ASIG
            | CONDICIONAL
            | TkFor TkId TkFrom EXPR TkTo EXPR TkHacer INSTGEN TkEnd
            | TkFor TkId TkFrom EXPR TkTo EXPR TkStep EXPR TkHacer INSTGEN TkEnd
            | TkWhile EXPR TkHacer INSTGEN TkEnd
            | INCALC
            | ENTRADASALIDA'''
    global tablaSimb
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 6:
        p[0] = cINST("ciclo indefinido",None,None,None,p[2],p[4],tablaSimb,6)
    elif len(p) ==10:
        p[0] = cINST("FOR",p[2],None,p[4],p[6],p[8],tablaSimb,10)
    else:
        p[0] = cINST("FORconStep",p[2],p[4],p[6],p[8],p[10],tablaSimb,11)
    
def p_CONDICIONAL(p):
    '''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''
    p[0] = cCondicional(p[2],p[4],p[5])

class cAuxcond:
    def __init__(self,insgen):
        self.type = "Otherwise"
        self.instgen = insgen
        self.arr = [self.instgen]
    # Transicion
    def verificar(self,tabla):
        self.instgen.verificar(tabla)

    def linkear_tablas(self):
        self.instgen.linkear_tablas(link)

def p_AUXCOND(p):
    '''AUXCOND : TkEnd
               | TkOtherwise TkHacer INSTGEN TkEnd'''
    if len(p)==2:

        p[0] = p[1]
    else:
        p[0] = cAuxcond(p[3])

def p_ASIG(p):
    '''ASIG : EXPR TkAsignacion EXPR TkPunto'''
    p[0] = cAsig(p[1],p[3])

def p_INCALC(p):
    '''INCALC : NEO'''
    global tablaSimb
    tabla = tablaSimb.copy()
    tablaSimb.clear()
    p[0] = cIncAlc(p[1],tabla)
    p[0].tabla = p[1].tabla

def p_ENTRADASALIDA(p):
    '''ENTRADASALIDA : TkPrint EXPR TkPunto
                     | TkRead EXPR TkPunto'''
    p[0] = cEntSal(p[1],p[2])

def p_SECUENC(p):
    '''SECUENC : INSTGEN INST'''
    p[0] = cSecu(p[1],p[2])

def p_INSTGEN(p):
    '''INSTGEN : SECUENC
               | INST'''
    p[0] = p[1]

def p_EXPR(p):
    '''EXPR : LITER
            | TkId
            | TkParAbre EXPR TkParCierra
            | EXPR TkSuma EXPR
            | EXPR TkResta EXPR
            | EXPR TkDiv EXPR
            | EXPR TkMult EXPR
            | EXPR TkMod EXPR
            | TkResta EXPR %prec UTkResta
            | EXPR TkConjuncion EXPR
            | EXPR TkDisyuncion EXPR
            | TkNegacion EXPR
            | EXPR TkSiguienteCar
            | EXPR TkAnteriorCar
            | TkValorAscii EXPR
            | EXPR TkConcatenacion EXPR
            | TkRotacion EXPR
            | TkTrasposicion EXPR
            | INDEXMAT
            | EXPR TkMayor EXPR
            | EXPR TkMenor EXPR
            | EXPR TkMayorIgual EXPR
            | EXPR TkMenorIgual EXPR
            | EXPR TkDesigual EXPR
            | EXPR TkIgual EXPR'''
    global tablaSimb
    if len(p)==2:
        if (not isinstance(p[1],cLitMat))and (not isinstance(p[1],cIndexMat)):
            p[0]=cExprUn(p[1],None,tablaSimb,len(p))
        else:
            p[0]=p[1]
    elif len(p)==4:
        if p[1]!="(":
            p[0] = cExprBin(p[1],p[2],p[3],tablaSimb)
        else:
            p[0] = cExprUn(p[2],None,tablaSimb,len(p))            
    elif len(p)==3:
        if p[2]=="++" or p[2]=="--":
            p[0] = cExprUn(p[1],p[2],tablaSimb,len(p))
        else:
            p[0] = cExprUn(p[2],p[1],tablaSimb,len(p)) 
              

def p_LITER(p):
    '''LITER : TkTrue
             | TkFalse
             | TkNum
             | TkCaracter
             | LITMAT'''
    p[0] = p[1]

def p_LITMAT(p):
    '''LITMAT : TkLlaveAbre AUXLITMAT TkLlaveCierra
              | TkLlaveAbre TkLlaveCierra'''
    if len(p)==3:
        p[0] = cLitMat(None)
        p[0].numDim = 1
    else:
        p[0] = cLitMat(p[2])
        if isinstance(p[2],cAuxLitMat):
            p[0].numDim = 1 + p[2].numDim
            p[0].tipobase = p[2].tipobase 
        elif isinstance(p[2],cLitMat):
            p[0].numDim = 1 + p[2].numDim
            p[0].tipobase = p[2].tipobase 
        else:
            p[0].tipobase = p[2].tipo
            p[0].numDim = 1

def p_AUXLITMAT(p):
    '''AUXLITMAT : EXPR TkComa AUXLITMAT
                 | EXPR'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = cAuxLitMat(p[1],p[3])
        if isinstance(p[3],cAuxLitMat):
            p[0].numDim = p[3].numDim
        elif isinstance(p[3],cLitMat):
            p[0].numDim = p[3].numDim
        else:
            p[0].numDim = 0

def p_INDEXMAT (p):
    '''INDEXMAT : EXPR TkCorcheteAbre DIM TkCorcheteCierra'''
    p[0] = cIndexMat(p[1],p[3])

def p_error(p):
    print("Syntax error at '%s'" % p.value)
    print("En la linea "+str(p.lineno))
    exit(0)


try:
    f = open(sys.argv[1],'r')
except:
    print("No se pudo abrir el archivo")
    exit(0)
#parser = yacc.yacc()
parser = yacc.yacc(start = 'NEO')
learcvhivo=f.read()
result= parser.parse(learcvhivo,lexer=lexy)
ITERADOR = [0]
def imprimir(result,i):
    if(isinstance(result,str)):
        print(i*" "+result)
    else:
        print(i*" "+result.type)
        if result.type == "FOR":
            print((i+2)*" "+"ITERADOR: "+result.identificador)
            print((i+2)*" "+"RANGO:")
            imprimir(result.exp2,i+2+2)
            print((i+2)*" "+"HASTA:")
            imprimir(result.exp3,i+2+2)
            print((i+2)*" "+"INSTRUCCION:")
            imprimir(result.instgen,i+2+2)
            j = 0
            ITERADOR[0] = 3 
        elif result.type == "ASIGNACION":
            print((i+2)*" "+"CONTENEDOR:")
            imprimir(result.expr_izq,i+2+2)
            print((i+2)*" "+"EXPRESION A ASIGNAR:")
            imprimir(result.expr_der,i+2+2)
            j = 0
            ITERADOR[0] = 3
        elif result.type == "Expresion Binaria":
            print((i+2)*" "+"EXPRESION IZQ:")
            imprimir(result.expr_izq,i+2+2)
            print((i+2)*" "+"OPERADOR: "+result.oper)
            print((i+2)*" "+"EXPRESION DER:")
            imprimir(result.expr_der,i+2+2)
            j = 0
            ITERADOR[0] = 3  
        else:
            #print(i*" "+result.type)
            j = i
            for elem in result.arr:
                if elem:
                    if(isinstance(elem,str)):
                        print(j*" "+elem)
                        j = i + 2
                    else:
                        if(elem.type):
                            imprimir(elem,i+2)
result.linkear_tablas(None)
result.verificar()
print(result.tabla)
#print(result.instgen.instgen.alc.instgen.instgen.tabla,"lol")
try:
    imprimir(result,0)
    print("end")
except:
    pass
