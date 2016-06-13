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
global tabla = dict()
class cNeo:
	def __init__(self,lis_dec,insgen,tabla):
		self.type = "NEO"
		self.list_dec = lis_dec
		self.instgen = insgen
		self.tabla = tabla
		self.arr = [self.list_dec,self.instgen]
def p_NEO(p):
    '''NEO : TkWith LIST_DEC TkBegin INSTGEN TkEnd
    	   | TkBegin INSTGEN TkEnd'''
    # Primer Caso:
    global tabla
    if p[1] == 'with':
        p[0] = cNeo(p[2],p[4],tabla)			# Nodo Parser :D
        #p[0].tabla = p[2].tabla			# A la tabla de Neo le asigno la tabla de LIST_DEC
        p[4].tabla = p[0].tabla			# Ahora a INSTGEN le pasamos la tabla de simbolos
    else:
        p[0] = cNeo(None,p[2])			# Nodo Parser :D
        p[2].tabla = p[0].tabla			# Ahora a INSTGEN le pasamos la tabla de simbolos        
    print(p[0].tabla)

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
        self.tabla = dict() 
        
def p_LIST_DEC(p):
    '''LIST_DEC : TkVar LIST_IDEN TkDosPuntos TIPO
                | LIST_DEC TkVar LIST_IDEN TkDosPuntos TIPO'''
    # Primer Caso:
    if p[1] == 'var':
        p[0] = cList_Dec(None,p[2],p[4])    			# Nodo Parser                            
        for ident in p[2].lista:						# Obtenemos la lista de identificadores
            if not p[0].tabla.__contains__(ident[0]):	# Si el elemento no esta, entonces verificamos el tipo
                if ident[1]==p[4] or ident[1]=="":						# Si el tipo es el correcto, entonces lo agregamos a la tabla
                    p[0].tabla[ident[0]] = p[4]			# Agregamos el elemento a la tabla con el tipo correspondiente.
                else:
                    print("Error de tipo: "+str(ident[0])+" de tipo "+str(p[4])+" pero se le asigno "+str(ident[1]))
                    exit(0)
            else:
                print("La variable "+str(ident[0])+" fue declarada anteriormente")
                exit(0)
    else:  
        p[0] = cList_Dec(p[1],p[3],p[5])    			# Nodo Parser
        p[0].tabla = p[1].tabla
        for ident in p[3].lista:						# Obtenemos la lista de identificadores
            if not p[0].tabla.__contains__(ident[0]):	# Si el elemento no esta, entonces verificamos el tipo
                if ident[1]==p[5] or ident[1]=="":		# Si el tipo es el correcto, entonces lo agregamos a la tabla
                    p[0].tabla[ident[0]] = p[5]			# Agregamos el elemento a la tabla con el tipo correspondiente.
                else:
                    print("Error de tipo: "+str(ident[0])+" de tipo "+str(p[5])+" pero se le asigno "+str(ident[1]))
                    exit(0)
            else:
                print("La variable "+str(ident[0])+" fue declarada anteriormente")
                exit(0)
class cTipo:
    def __init__(self,dim,tipo):
        self.type = "Matriz"
        self.dim = dim
        self.tipo = tipo
        self.tabla = dict()
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
        self.tabla = dict()
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
        self.tabla = dict()
        self.lista = []
        
def p_LIST_IDEN(p):
    '''LIST_IDEN : TkId OPASIG
                 | LIST_IDEN TkComa TkId OPASIG'''
    # Primer Caso:
    if len(p) == 3:
        p[0] = cList_Iden(None,p[2],p[1])   			# Nodo parser
        if p[2]!="":
            p[0].lista = [(p[1],p[2].tipo)]					# Caso base :D
        else:
            p[0].lista = [(p[1],"")]
    else:
        p[0] = cList_Iden(p[1],p[4],p[3])               # Nodo Parser :D
        if p[4]!="":
            p[0].lista = p[1].lista + [(p[3],p[4].tipo)]# A lo que llevamos de la lista anterior. le pegamos lo ultimo
        else:
            p[0].lista = p[1].lista + [(p[3],"")]
    
class cOpasig:
    def __init__(self,expr):
        self.type = "OPASIG"
        self.expr = expr
        self.tabla = dict()
        self.arr = [self.expr]
        self.tipo = None
        
def p_OPASIG(p):
    '''OPASIG : TkAsignacion EXPR
              | empty'''
    if len(p) == 3:
        p[0] = cOpasig(p[2])
        p[0].tipo = p[2].tipo
        
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

def p_CONDICIONAL(p):
	'''CONDICIONAL : TkIf EXPR TkHacer INSTGEN AUXCOND'''
	p[0] = cCondicional(p[2],p[4],p[5])

class cAuxcond:
	def __init__(self,insgen):
		self.type = "Otherwise"
		self.instgen = insgen
		self.arr = [self.instgen]

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

def p_ENTRADASALIDA(p):
	'''ENTRADASALIDA : TkPrint EXPR TkPunto
					 | TkRead EXPR TkPunto'''
	print("TUPAPA")
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
	def __init__(self,expr_izq,oper,expr_der):
		self.type = "Expresion Binaria"
		self.expr_izq = expr_izq
		#if oper in {"+","-","*","/","%"}:
		#	self.type = "Expresion Aritmetica"
		#elif oper in {"/\\","\\/"}:
		#	self.type = "Expresion Booleana"
		#elif oper in {"::"}:
		#	self.type = "Concatenacion Matrices"
		#elif oper in {"<",">","<=",">=","=","/=",}:
		#	self.type = "Expresion Relacional"
		self.oper = oper
		self.expr_der = expr_der
		self.arr = [self.expr_izq,self.oper,self.expr_der]

class cExprUn:
	def __init__(self,expr,oper):
		self.type = "Expresion Unaria"
		self.oper = oper
		self.expr = expr
		self.arr = [self.oper, self.expr]
		self.tipo = None
		self.subir = []

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

	if len(p)==2:
		p[0]=cExprUn(p[1],None)
		if isinstance(p[1],str):
			print(p[1])
			if p[1].isnumeric():
				p[0].tipo = "int"
			elif p[1][0] == '\'':	
				p[0].tipo = "char"
			elif p[1] == "True" or p[1] == "False":
				p[0].tipo = "bool"
			else:
				n=len(p)
				i = -1
				while i>-n:
					if isinstance(p[i], cList_Dec):
						if p[i].tabla.__contains__(p[1]):
							p[0].tipo = p[i].tabla[p[1]]
							break
					i = i - 1
				if i==-n:
					print("Hola")
					print("Error, "+str(p[1])+" no fue declarada")
					exit(0)
		#else MATRIZ

	elif len(p)==4:
		if p[1]!="(":
			p[0] = cExprBin(p[1],p[2],p[3])
	elif len(p)==3 or (len(p)==4 and p[1]=="("):
		if p[1]=="(":
			p[0] = p[2]
		else:
			derecha=True #Donde esta la expresion
			hayHoja = False 	#Hojas son literales
			valorAscii = False
			
			if p[1]=="-":
				p[0] = cExprUn(p[2],p[1])
				p[0].tipo = "int"
				if isinstance(p[2],basestring):
					if p[2].isnumeric():
						p[0].subir.append(p[2])
						hayHoja = True

			elif p[1]=="#":
				valorAscii = True
				p[0] = cExprUn(p[2],p[1])
				p[0].tipo = "int"
				if isinstance(p[2],basestring):
					if p[2][0] == '\'':		
						p[0].subir.append(p[2])
						hayHoja = True								

			elif p[1]=="not":
				p[0] = cExprUn(p[2],p[1])
				p[0].tipo = "bool"
				if isinstance(p[2],basestring):
					if p[2] == "True" or p[2] == "False":		
						p[0].subir.append(p[2])
						hayHoja = True	

			elif p[2]=="++" or p[2]=="--":
				p[0] = cExprUn(p[1],p[2])
				p[0].tipo = "char"
				if isinstance(p[1],basestring):
					if p[1][0] == '\'':		
						p[0].subir.append(p[1])
						hayHoja = True
				derecha=False

			if not hayHoja:
				if derecha:
					if isinstance(p[2],basestring):
						if p[2] == "True" or p[2] == "False" or p[2][0] == '\'' or p[2].isnumeric():
							print("Error de tipo en derecha TkId")
							exit(0)
						else:
							n=len(p)
							i = -1
							while i>-n:
								if isinstance(p[i], cList_Dec):
									if p[i].tabla.__contains__(p[2]):
										if p[i].tabla[p[2]]!=p[0].tipo:
											if (not valorAscii):
												print("Error de tipo, objeto "+str(p[2])+" no es de tipo "+str(p[0].tipo))
												exit(0)
											else:
												if p[i].tabla[p[2]]!="char":
													print("Error de tipo, objeto "+str(p[2])+" no es de tipo char")
													exit(0)
												else:
													p[0].subir.append((p[2],p[0].tipo))			
										else:
											if (not valorAscii):
												p[0].subir.append((p[2],p[0].tipo))
											else:
												print("Error de tipo, objeto "+str(p[2])+" no es de tipo char")
												exit(0)
										break
								i = i - 1
							if i==-n:
								print("Error, "+str(p[2])+" no fue declarada")
								exit(0)
					else:
						if(p[0].tipo!=p[2].tipo):
							print("Error de tipo, operando tipo "+str(p[2].tipo)+" como tipo "+p[0].tipo)
							exit(0)
						p[0].subir = p[2].subir
				else:
					if isinstance(p[1],basestring):
						if p[1] == "True" or p[1] == "False" or p[1][0] == '\'' or p[1].isnumeric():
							print("Error de tipo en derecha TkId")
							exit(0)
						else:
							n=len(p)
							i = -1
							while i>-n:
								if isinstance(p[i], cList_Dec):
									if p[i].tabla.__contains__(p[1]):
										if p[i].tabla[p[1]]!=p[0].tipo:
											print("Error de tipo, objeto "+str(p[1])+" no es de tipo "+str(p[0].tipo))
											exit(0)
										else:
											p[0].subir.append((p[1],p[0].tipo))
										break
								i = i - 1
							if i==-n:
								print("Error, "+str(p[1])+" no fue declarada")
								exit(0)
					else:
						if(p[0].tipo!=p[1].tipo):
							print("Error de tipo, operando tipo "+str(p[1].tipo)+" como tipo "+p[0].tipo)
							exit(0)
						p[0].subir = p[1].subir
	
	##########	SUBIR EN EL ARBOL #########
	#i = -1
	#while True:
	#	if isinstance(p[i], cList_Dec):
	#		print(p[i])
	#		break
	#	i = i - 1
	######################################

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
		self.arr = [self.val]

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

def imprimir(result,i):
	print(i*" "+result.type)
	j = i
	for elem in result.arr:
		if elem:
			if(isinstance(elem,str)):
				j = i + 4
				print(j*" "+elem)
					
			else:
				imprimir(elem,i+4)
try:
	imprimir(result,0)
	print("end")
except:
	pass
  
  
"""
var i <- 5, j<-i : int
var j<-i, i<-5 : int


 a,i=i,5
 
 
%%NEHRO MAMAMA HEUVO
with
	var n <- 5 : int
begin 
	n<-2+2.
end
"""
