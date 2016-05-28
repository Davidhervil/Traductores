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
class cNeo:
	def __init__(self,lis_dec,insgen):
		self.type = "NEO"
		self.list_dec = lis_dec
		self.instgen = insgen
		self.arr = [self.list_dec,self.instgen]
def p_NEO(p):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
    	   | TkBegin INSTGEN TkEnd''' 
    if p[1] == 'with':
    	p[0] = cNeo(p[2],p[4])
    else:
    	p[0] = cNeo(None,p[2])


def p_empty(p):
    '''empty :'''
    pass

class cList_Dec:
	def __init__(self, lis_dec, lis_iden, tipo):
		self.type = "LISTA DE DECLARACION"
		self.list_dec = lis_dec
		self.list_iden = lis_iden
		self.tipo = tipo
		self.arr = [self.list_dec,self.list_iden,self.tipo]
def p_LIST_DEC(p):
	'''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
				| LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''
	if p[1] == 'var':
		p[0] = cList_Dec(None,p[2],p[4])
	else:
		p[0] = cList_Dec(p[1],p[3],p[5])

class cTipo:
	def __init__(self,dim,tipo):
		self.type = "Matriz"
		self.dim = dim
		self.tipo = tipo
		self.arr = [self.dim,self.tipo]
def p_TIPO(p):
	'''TIPO : TkInt
	     	| TkBool
	      	| TkChar
	     	| TkMatrix TkCorcheteAbre DIM TkCorcheteCierra TkOf TIPO'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = cTipo(p[3],p[6])


class cDim:
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
	def __init__(self,lis_iden,opasig,ident):
		self.type = "LISTA DE IDENTIFICADORES"
		self.lis_iden = lis_iden
		self.expr = opasig
		self.ident = ident
		self.arr = [self.lis_iden,self.expr,self.ident]
def p_LIST_IDEN(p):
	'''LIST_IDEN : TkId OPASIG
			     | LIST_IDEN TkComa TkId OPASIG'''
	if len(p) == 3:
		p[0] = cList_Iden(None,p[2],p[1])
	else:
		p[0] = cList_Iden(p[1],p[4],p[3])

class cOpasig:
	def __init__(self,expr):
		self.type = "OPASIG"
		self.expr = expr
		self.arr = [self.expr]
def p_OPASIG(p):
	'''OPASIG : TkAsignacion EXPR
			  | empty'''
	if len(p) == 3:
		p[0] = cOpasig(p[2])
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

def p_CONDICIONAL(p):
	'''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''
	p[0] = cCondicional(p[2],p[4],p[5])

class cAuxcond:
	def __init__(self,insgen):
		self.type = "Otherwise"
		self.instgen = insgen

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
def p_ASIG(p):
	'''ASIG : EXPR TkAsignacion EXPR TkPunto'''
	p[0] = cAsig(p[1],p[3])

class cIncAlc:
	def __init__(self,param):
		self.type = "INCORPORACION DE ALCANCE"
		self.alc = param

def p_INCALC(p):
	'''INCALC : NEO'''
	p[0] = cIncAlc(p[1])

class cEntSal:
	def __init__(self,io,expr):
		self.type = "ENTRADA SALIDA"
		self.expr = expr
		self.io = io
		self.arr = [self.expr, self.io]

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

def p_SECUENC(p):
	'''SECUENC : INSTGEN INST'''
	p[0] = cSecu(p[1],p[2])

def p_INSTGEN(p):
	'''INSTGEN : SECUENC
			   | INST'''
	p[0] = p[1]

class cExprBin:
	def __init__(self,expr_izq,oper,):
		self.type = "Expresion Binaria"
		self.expr_izq = expr_izq
		if oper in {"+","-","*","/","%"}:
			self.type = "Expresion Aritmetica"
		elif oper in {"/\\","\\/"}:
			self.type = "Expresion Booleana"
		else:
			pass #OJOOOJOJO
		self.expr_der = expr_der
		self.arr = [self.expr_izq,self.oper,self.expr_der]


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
	for t in p:
		if(not (t is None)):
			print(t)

	if len(p)==2:
		p[0]=p[1]

def p_LITER(p):
	'''LITER : TkTrue
			 | TkFalse
			 | TkNum
			 | TkCaracter
			 | LITMAT'''
	p[0] = p[1]

class cLitMat:
	def __init__(self,auxlitmat):
		self.type = "Literl Matriz"
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
		self.valor = expr + "[" + dim.valor + "]"
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
def imprimir(result,i):
	print(i*" "+result.type)
	j = i
	for elem in result.arr:
		if elem:
			if(isinstance(elem,str)):
				print(j*" "+elem)
				j = i + 4
			else:
				imprimir(elem,i+4)

imprimir(result,0)
print("end")
