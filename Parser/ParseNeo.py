from LexNeo import tokens
from LexNeo import reservados
import ply.yacc as yacc

start = 'Neo'
precedence = (
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv'),
    ('left','TkMod'),
    ('right', 'TkUResta'),            # Unary minus operator
)

def p_Neo(t):
    '''Neo : TkWith LIST_DEC TkBegin INST TkEnd
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
			| EXPR TkCorcheteAbre DIM TkCorcheteCierra TkAsignacion EXPR TkPunto'''

def p_INCALC(t):
	'''INCALC : NEO'''

def p_ENTRADASALIDA(t):
	'''ENTRADASALIDA : TkPrint EXPR TkPunto
					 | TkRead TkId TkPunto'''

def p_SECUENC(t):
	'''SECUENC : INST INST'''

def p_EXPR(t):
	'''EXPR : LITER'''

def p_LITER(t):
	'''LITER : TkTrue
			 | TkFalse
			 | TkNum
			 | TkCaracter
			 | LITMAT'''

def p_LITMAT(t):
	'''LITMAT : TkLlaveAbre AUXLITMAT TkLlaveCierra
			  | TkLlaveAbre TkLlaveCierra
			  | EXPR'''

def p_AUXLITMAT(t):
	'''AUXLITMAT : TkLlaveAbre TkLlaveCierra
			  	 | EXPR''' 
parser = yacc.yacc(start = 'Neo')
