from LexNeo import tokens
from LexNeo import reservados
import ply.yacc as yacc

start = 'NEO'
precedence = (
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv'),
    ('left','TkMod'),
    ('right', 'UTkResta'),            # Unary minus operator
)

def p_NEO(t):
    '''NEO : TkWith LIST_DEC TkBegin INST TkEnd
    	   | TkBegin INST TkEnd''' 

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
		    | TkIf EXPR TkHacer INST TkEnd
			| TkIf EXPR TkHacer INST TkOtherwise TkHacer INST TkEnd
			| TkFor TkId TkFrom EXPR TkTo EXPR TkHacer INST TkEnd
			| TkFor TkId TkFrom EXPR TkTo EXPR TkStep EXPR TkHacer INST TkEnd
			| TkWhile EXPR TkHacer INST TkEnd
			| INCALC
			| ENTRADASALIDA
			| SECUENC'''

def p_ASIG(t):
	'''ASIG : TkId TkAsignacion EXPR TkPunto
			| INDEXMAT TkAsignacion EXPR TkPunto'''

def p_INCALC(t):
	'''INCALC : NEO'''

def p_ENTRADASALIDA(t):
	'''ENTRADASALIDA : TkPrint EXPR TkPunto
					 | TkRead EXPR TkPunto'''

def p_SECUENC(t):
	'''SECUENC : INST INST'''

def p_EXPR(t):
	'''EXPR : LITER
			| TkId
			| TkParAbre EXPR TkParCierra
			| EXPRARIT
			| EXPRBOOL
			| EXPRCAR
			| EXPRMAT
			| EXPRREL'''

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

def p_EXPRARIT(t):
	'''EXPRARIT : EXPR TkSuma EXPR
				| EXPR TkResta EXPR
				| EXPR TkDiv EXPR
				| EXPR TkMult EXPR
				| EXPR TkMod EXPR
				| TkResta EXPR %prec UTkResta'''

def p_EXPRBOOL(t):
	'''EXPRBOOL : EXPR TkConjuncion EXPR
				| EXPR TkDisyuncion EXPR
				| TkNegacion EXPR'''

def p_EXPRCAR(t):
	'''EXPRCAR : EXPR TkSiguienteCar
			   | EXPR TkAnteriorCar
			   | TkValorAscii EXPR'''

def p_EXPRMAT(t):
	'''EXPRMAT : EXPR TkConcatenacion EXPR
			   | TkRotacion EXPR
			   | TkTrasposicion EXPR
			   | INDEXMAT'''

def p_INDEXMAT (t):
	'''INDEXMAT : EXPR TkCorcheteAbre DIM TkCorcheteCierra'''

def p_EXPRREL(t):
	'''EXPRREL : EXPR TkMayor EXPR
			   | EXPR TkMenor EXPR
			   | EXPR TkMayorIgual EXPR
			   | EXPR TkMenorIgual EXPR
			   | EXPR TkDesigual EXPR'''

def p_error(t):
	print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(start = 'NEO')
