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

def p_NEO(p):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
    	   | TkBegin INSTGEN TkEnd''' 

def p_empty(p):
    '''empty :'''
    pass

def p_LIST_DEC(p):
	'''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
				| LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''

def p_TIPO(p):
	'''TIPO : TkInt
	     	| TkBool
	      	| TkChar
	     	| TkMatrix TkCorcheteAbre DIM TkCorcheteCierra TkOf TIPO'''

def p_DIM(p):
	'''DIM  : EXPR
			| DIM TkComa EXPR'''

def p_LIST_IDEN(p):
	'''LIST_IDEN : TkId OPASIG
			     | LIST_IDEN TkComa TkId OPASIG'''

def p_OPASIG(p):
	'''OPASIG : TkAsignacion EXPR
			  | empty'''

def p_INST(p):
	'''INST : ASIG
		    | CONDICIONAL
			| TkFor TkId TkFrom EXPR TkTo EXPR TkHacer INSTGEN TkEnd
			| TkFor TkId TkFrom EXPR TkTo EXPR TkStep EXPR TkHacer INSTGEN TkEnd
			| TkWhile EXPR TkHacer INSTGEN TkEnd
			| INCALC
			| ENTRADASALIDA'''

def p_CONDICIONAL(p):
	'''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''

def p_AUXCOND(p):
	'''AUXCOND : TkEnd
			   | TkOtherwise TkHacer INSTGEN TkEnd'''

def p_ASIG(p):
	'''ASIG : EXPR TkAsignacion EXPR TkPunto'''

def p_INCALC(p):
	'''INCALC : NEO'''

def p_ENTRADASALIDA(p):
	'''ENTRADASALIDA : TkPrint EXPR TkPunto
					 | TkRead EXPR TkPunto'''

def p_SECUENC(p):
	'''SECUENC : INSTGEN INST'''

def p_INSTGEN(p):
	'''INSTGEN : SECUENC
			   | INST'''

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

def p_LITER(p):
	'''LITER : TkTrue
			 | TkFalse
			 | TkNum
			 | TkCaracter
			 | LITMAT'''

def p_LITMAT(p):
	'''LITMAT : TkLlaveAbre AUXLITMAT TkLlaveCierra
			  | TkLlaveAbre TkLlaveCierra'''

def p_AUXLITMAT(p):
	'''AUXLITMAT : EXPR TkComa AUXLITMAT
			  	 | EXPR'''

def p_INDEXMAT (p):
	'''INDEXMAT : EXPR TkCorcheteAbre DIM TkCorcheteCierra'''

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
parser.parse(learcvhivo,lexer=lexy)
