from LexNeo import tokens,reservados,lexy
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
global tablaSimb
tablaSimb = dict()

class cNeo:
    def __init__(self,lis_dec,insgen,tabla):
        self.type = "NEO"
        self.list_dec = lis_dec
        self.instgen = insgen
        self.tabla = tabla
        self.arr = [self.list_dec,self.instgen]
    def verificar(self):
        if self.list_dec != None:
            self.list_dec.verificar()
        self.instgen.verificar()
        print(self.tabla)

def p_NEO(p):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
           | TkBegin INSTGEN TkEnd''' 
    global tablaSimb
    if p[1] == 'with':
        p[0] = cNeo(p[2],p[4],tablaSimb)
    else:
        p[0] = cNeo(None,p[2],tablaSimb)

def p_empty(p):
    '''empty :'''
    pass

class cList_Dec:
    def __init__(self, lis_dec, lis_iden, tipo,tabla):
        self.type = "LISTA DE DECLARACION"
        self.list_dec = lis_dec
        self.list_iden = lis_iden
        self.tipo = tipo
        self.arr = [self.list_dec,self.list_iden,self.tipo]
        self.tabla = tabla
    def verificar(self):
        if self.list_dec != None:
            self.list_dec.verificar()
        self.list_iden.verificar()
def p_LIST_DEC(p):
    '''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
                | LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''
    global tablaSimb
    if p[1] == 'var':
        p[0] = cList_Dec(None,p[2],p[4],tablaSimb)                # Nodo Parser                            
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
        p[0] = cList_Dec(p[1],p[3],p[5],tablaSimb)                # Nodo Parser
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

class cTipo:
    def __init__(self,dim,tipo,tabla):
        self.type = "Matriz"
        self.dim = dim
        self.tipo = tipo
        self.arr = [self.dim,self.tipo]
        self.tabla = tabla
def p_TIPO(p):
    '''TIPO : TkInt
            | TkBool
            | TkChar
            | TkMatrix TkCorcheteAbre DIM TkCorcheteCierra TkOf TIPO'''
    global tablaSimb
    if len(p) == 2:
        p[0] = p[1]                         #### QUIZAS HAGA FALTA HACERLO CLASE TAMBIEN (COMO EN EXPRESION)
    else:
        p[0] = cTipo(p[3],p[6],tablaSimb )

class cDim:                                 ### ARREGLAR ESTO PARA DIMENSIONES CHEVERONGAS
    def __init__(self,dim,expr):
        self.type = "DIMENSION"
        self.valor = dim + "," + expr
        self.arr = [self.valor]
def p_DIM(p):
    '''DIM  : EXPR
            | DIM TkComa EXPR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = cDim(p[1],p[3])


class cList_Iden:
    def __init__(self,lis_iden,opasig,ident,tabla,tam):
        self.type = "LISTA DE IDENTIFICADORES"
        self.lis_iden = lis_iden
        self.expr = opasig
        self.ident = ident
        self.arr = [self.lis_iden,self.expr,self.ident]
        self.lista = []
        self.tabla = tabla
        self.tam = tam
        
    def verificar(self):
        if self.lis_iden:    
            self.lis_iden.verificar()
        if self.expr!="":
            self.expr.verificar()
            if self.expr.tipo != self.tabla[self.ident]:
                print("Error de tipo: "+str(self.ident)+" de tipo "+str(self.tabla[self.ident])+" pero se le asigno "+str(self.expr.tipo))
                exit(0)
                  
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

class cOpasig:
    def __init__(self,expr,tabla):
        self.type = "OPASIG"
        self.expr = expr
        self.arr = [self.expr]
        self.tabla = tabla
        
    def verificar(self):
        self.expr.verificar()
        self.tipo=self.expr.tipo
        
def p_OPASIG(p):
    '''OPASIG : TkAsignacion EXPR
              | empty'''
    global tablaSimb
    if len(p) == 3:
        p[0] = cOpasig(p[2],tablaSimb)
    else:
        p[0] = ""


class cINST:
    def __init__(self,tipoAux,ident,exp1,exp2,exp3,insgen):
        self.type = tipoAux
        self.identificador = ident
        self.exp1 = exp1
        self.exp2 = exp2
        self.exp3 = exp3
        self.instgen = insgen
        self.arr = [self.identificador,self.exp1,self.exp2,self.exp3,self.instgen]
def p_INST(p):
    '''INST : ASIG
            | CONDICIONAL
            | TkFor TkId TkFrom EXPR TkTo EXPR TkHacer INSTGEN TkEnd
            | TkFor TkId TkFrom EXPR TkTo EXPR TkStep EXPR TkHacer INSTGEN TkEnd
            | TkWhile EXPR TkHacer INSTGEN TkEnd
            | INCALC
            | ENTRADASALIDA'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 6:
        p[0] = cINST("ciclo indefinido",None,None,None,p[2],p[4])
    elif len(p) ==10:
        p[0] = cINST("FOR",p[2],None,p[4],p[6],p[8])
    else:
        p[0] = cINST("FORconStep",p[2],p[4],p[6],p[8],p[10])

class cCondicional:
    def __init__(self,expr,instgen,auxcond):
        self.type = "CONDICIONAL"
        self.guardia = expr
        self.instgen = instgen
        self.other = auxcond
        self.arr = [self.guardia,self.instgen,self.other]
        
    def verificar(self):
        self.guardia.verificar()
        if self.guardia.tipo!="bool":
            print("Error, guardia de tipo "+self.guardia.tipo+" en lugar de bool.")
            exit(0)
        self.instgen.verificar.()
        self.other.verificar()
        
def p_CONDICIONAL(p):
    '''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''
    p[0] = cCondicional(p[2],p[4],p[5])

class cAuxcond:
    def __init__(self,insgen):
        self.type = "Otherwise"
        self.instgen = insgen
        self.arr = [self.instgen]
    def verificar(self):
        self.instgen.verificar()

def p_AUXCOND(p):
    '''AUXCOND : TkEnd
               | TkOtherwise TkHacer INSTGEN TkEnd'''
    if len(p)==2:

        p[0] = p[1]
    else:
        p[0] = cAuxcond(p[3])

class cAsig:
    def __init__(self,expr_izq,expr_der):
        self.type = "ASIGNACION"
        self.expr_izq= expr_izq
        self.expr_der = expr_der
        self.arr = [self.expr_izq,self.expr_der]
    
    def verificar(self):
        self.expr_izq.verificar()
        self.expr_der.verificar()
        if self.expr_izq.tipo != self.expr_der.tipo:
            print("Error, asignando a "+str(self.expr_izq.tipo)+" tipo "+str(self.expr_izq.tipo)
        
def p_ASIG(p):
    '''ASIG : EXPR TkAsignacion EXPR TkPunto'''
    p[0] = cAsig(p[1],p[3])

class cIncAlc:
    def __init__(self,param):
        self.type = "INCORPORACION DE ALCANCE"
        self.alc = param
        self.arr = [self.alc]

def p_INCALC(p):
    '''INCALC : NEO'''
    p[0] = cIncAlc(p[1])

class cEntSal:
    def __init__(self,io,expr):
        self.type = "ENTRADA SALIDA"
        self.expr = expr
        self.io = io
        self.arr = [self.expr, self.io]
    def verificar(self):
        self.expr.verificar()

def p_ENTRADASALIDA(p):
    '''ENTRADASALIDA : TkPrint EXPR TkPunto
                     | TkRead EXPR TkPunto'''
    p[0] = cEntSal(p[1],p[2])
                  
class cSecu:
    def __init__(self,instgen,inst):
        self.type = "SECUENCIACION"
        self.instgen = instgen
        self.inst = inst
        self.arr = [self.instgen,self.inst]
    
    def verificar(self):
        self.instgen.verificar()
        self.instgen.verificar()

def p_SECUENC(p):
    '''SECUENC : INSTGEN INST'''
    p[0] = cSecu(p[1],p[2])

def p_INSTGEN(p):
    '''INSTGEN : SECUENC
               | INST'''
    p[0] = p[1]

class cExprBin:
    def __init__(self,expr_izq,oper,expr_der,tabla):
        self.type = "Expresion Binaria"
        self.expr_izq = expr_izq
        #elif oper in {"::"}:
        #   self.type = "Concatenacion Matrices"
        self.oper = oper
        self.expr_der = expr_der
        self.arr = [self.expr_izq,self.oper,self.expr_der]
        self.tabla = tabla
        self.tipo = None
    def verificar(self):
        self.expr_izq.verificar()
        self.expr_der.verificar()
        if self.oper in {"+","-","*","/","%"}:
            if self.expr_der.tipo == "int" and self.expr_izq.tipo == "int":
                self.tipo = "int"
            else:
                print("Error de tipo, operando "+self.expr_izq.tipo+" no es comparable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)
        elif self.oper in {"/\\","\\/"}:
            if self.expr_der.tipo == "bool" and self.expr_izq.tipo == "bool":
                self.tipo = "bool"
            else:
                print("Error de tipo, operando "+self.expr_izq.tipo+" no es comparable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)
        elif self.oper in {"<",">","<=",">=","=","/=",}:
            if (expr_der.tipo == "int" and expr_izq.tipo == "int") or (expr_der.tipo == "char" and expr_izq.tipo == "char") :
                self.tipo = "bool"
            else:
                print("Error de tipo, operando "+self.expr_izq.tipo+" no es comparable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)

class cExprUn:
    def __init__(self,expr,oper,tabla,tam):
        self.type = "Expresion Unaria"
        self.oper = oper
        self.expr = expr
        self.arr = [self.oper, self.expr]
        self.tipo = None
        self.tabla = tabla
        self.tam = tam

    def verificar(self):
        # CASO LITERALES O ID
        if self.tam == 2:           # Caso literales o TkId
            if isinstance(self.expr,str) and self.oper == None:
                if self.expr.isnumeric():
                    self.tipo = "int"
                elif self.expr[0] == '\'':   
                    self.tipo = "char"
                elif self.expr == "True" or self.expr == "False":
                    self.tipo = "bool"
                else:
                    if self.tabla.__contains__(self.expr):
                        self.tipo = p[i].tabla[self.expr]
                    else:
                        print("Error, "+str(self.expr)+" no fue declarada")
                        exit(0)
        # CASO UNARIOS
        elif self.tam == 3:
            self.expr.verificar()
            if self.oper=="-":
                if self.expr.tipo == "int":
                    self.tipo = "int" 
                else:
                    print("Error de tipo, operando "+self.expr.tipo+" como int.")
                    exit(0)
            elif self.oper=="#":  
                if self.expr.tipo == "char":
                    self.tipo = "int" 
                else:
                    print("Error de tipo, operando "+self.expr.tipo+" como char.")
                    exit(0)
            elif self.oper=="not":
                if self.expr.tipo == "bool":
                    self.tipo = "bool" 
                else:
                    print("Error de tipo, operando "+self.expr.tipo+" como bool.")
                    exit(0)
            elif self.oper=="++" or self.oper=="--": 
                if self.expr.tipo == "char":
                    self.tipo = "char" 
                else:
                  print("Error de tipo, operando "+self.expr.tipo+" como char.")
                  exit(0)
        
        # CASO PARENTESIS.
        else:                       # Caso parentesis.
            self.expr.verificar()
            self.tipo = self.expr.tipo

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
        p[0]=cExprUn(p[1],None,tablaSimb,len(p))
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

class cLitMat:
    def __init__(self,auxlitmat):
        self.type = "Literal Matriz"
        self.valor = "{" + auxlitmat + "}"
        self.arr = [self.valor]

def p_LITMAT(p):
    '''LITMAT : TkLlaveAbre AUXLITMAT TkLlaveCierra
              | TkLlaveAbre TkLlaveCierra'''
    if len(p)==2:
        p[0] = p[1] + p[2]
    else:
        p[0] = cLitMat(p[2])

class cAuxLitMat:
    def __init__(self,expr,auxlitmat):
        self.val = expr + "," + auxlitmat

def p_AUXLITMAT(p):
    '''AUXLITMAT : EXPR TkComa AUXLITMAT
                 | EXPR'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = cAuxLitMat(p[1],p[3]).val

class cIndexMat:
    def __init__(self,expr,dim):
        self.type = "Indexacion de Matrices"
        self.mati = expr
        self.indice = dim
        self.arr = [self.mati,self.indice]

def p_INDEXMAT (p):
    '''INDEXMAT : EXPR TkCorcheteAbre DIM TkCorcheteCierra'''
    p[0] = cIndexMat(p[1],p[3])

def p_error(p):
    print("Syntax error at '%s'" % p.value)
    print(p.lineno)

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
            print((i+2)*" "+"EXPRESION IZQ:")
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
try:
    imprimir(result,0)
    print("end")
except:
    pass
print(result.verificar())
