from LexNeo import tokens
from LexNeo import reservados
import ply.yacc as yacc

start = 'NEO'
precedence = (
    ('nonassoc','TkIgual','TkDesigual','TkMayor','TkMenor','TkMayorIgual','TkMenorIgual'),
    ('left', 'TkSuma', 'TkResta','TkConcatenacion', 'TkDisyuncion'),
    ('left', 'TkMult', 'TkDiv','TkConjuncion','TkRotacion'),
    ('left','TkMod','TkSiguienteCar','TkAnteriorCar'),
    ('right', 'UTkResta','TkNegacion','TkTrasposicion',), 
    ('nonassoc','TkValorAscii')           # Unary minus operator
)

def p_NEO(t):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
    	   | TkBegin INSTGEN TkEnd''' 

def p_LIST_DEC(t):
	'''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
				| LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''

def p_TIPO(t):
	'''TIPO : TkInt
	     	| TkBool
	      	| TkChar
	     	| TkMatrix TkCorcheteAbre DIM TkCorcheteCierra TkOf TIPO'''

def p_DIM(t):
	'''DIM  : EXPR
			| DIM TkComa EXPR'''

def p_LIST_IDEN(t):
	'''LIST_IDEN : TkId
			     | TkId TkAsignacion EXPR
			     | LIST_IDEN TkComa TkId
			     | LIST_IDEN TkComa TkId TkAsignacion EXPR'''

def p_INST(t):
	'''INST : ASIG
		    | CONDICIONAL
			| TkFor TkId TkFrom EXPR TkTo EXPR TkHacer INSTGEN TkEnd
			| TkFor TkId TkFrom EXPR TkTo EXPR TkStep EXPR TkHacer INSTGEN TkEnd
			| TkWhile EXPR TkHacer INSTGEN TkEnd
			| INCALC
			| ENTRADASALIDA'''

def p_CONDICIONAL(t):
	'''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''

def p_AUXCOND(t):
	'''AUXCOND : TkEnd
			   | TkOtherwise TkHacer INSTGEN TkEnd'''

def p_ASIG(t):
	'''ASIG : EXPR TkAsignacion EXPR TkPunto'''

def p_INCALC(t):
	'''INCALC : NEO'''

def p_ENTRADASALIDA(t):
	'''ENTRADASALIDA : TkPrint EXPR TkPunto
					 | TkRead EXPR TkPunto'''

def p_SECUENC(t):
	'''SECUENC : INSTGEN INST'''

def p_INSTGEN(t):
	'''INSTGEN : SECUENC
			   | INST'''

def p_EXPR(t):
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

def p_LITER(t):
	'''LITER : TkTrue
			 | TkFalse
			 | TkNum
			 | TkCaracter
			 | LITMAT'''

def p_LITMAT(t):
	'''LITMAT : TkLlaveAbre AUXLITMAT TkLlaveCierra
			  | TkLlaveAbre TkLlaveCierra'''

def p_AUXLITMAT(t):
	'''AUXLITMAT : EXPR TkComa AUXLITMAT
			  	 | EXPR'''

def p_INDEXMAT (t):
	'''INDEXMAT : EXPR TkCorcheteAbre DIM TkCorcheteCierra'''

def p_error(t):
	print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(start = 'NEO')
