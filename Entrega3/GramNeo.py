
"""
GramNeo.py
 Fecha : 17/06/2016
 Autores:
    David Hernandez     12-10761
    Arturo Toro         12-10796

 Descripcion: Objetos empleados para construir el AST junto a metodos que
 permiten detectar errores de tipo estaticos
"""

#---------------------------------------------------------------------------#
#                                   NODO                                    #
#---------------------------------------------------------------------------#
class Nodo:
    def __init__(self,padre,tabla):
        self.padre=padre            # Apunta al nodo anterior.
        self.tabla=tabla            # Contiene la tabla correspondiente al alcance.

#############################################################################
#                                   NEO                                     #
#############################################################################
class cNeo:
    def __init__(self,lis_dec,insgen,tabla):
        self.type = "NEO"
        self.list_dec = lis_dec
        self.instgen = insgen
        self.tabla = tabla
        self.arr = [self.list_dec,self.instgen]
        self.link = None
    def linkear_tablas(self,link):                      
        self.link = Nodo(link,self.tabla)               # Crear un nodo nuevo para alcance
        if self.list_dec:                               # Si hay declaraciones.
            self.list_dec.linkear_tablas(self.link)     #   Pasamos el link de alcance
        self.instgen.linkear_tablas(self.link)          # Pasamos el link a INSTGEN
    # Transicion
    def verificar(self):
        if self.list_dec != None:                       # Si hay Lista de Declaraciones
            self.list_dec.verificar(self.link.tabla)    #   Realizo sus verificaciones
        self.instgen.verificar(self.link.tabla)         # Verificaciones de INSTGEN

#############################################################################
#                           LISTA DE DECLARACIONES                          #
#############################################################################
class cList_Dec:
    def __init__(self, lis_dec, lis_iden, tipo,tabla):
        self.type = "LISTA DE DECLARACION"
        self.list_dec = lis_dec
        self.list_iden = lis_iden
        self.tipo = tipo
        self.arr = [self.list_dec,self.list_iden,self.tipo]
        self.tabla = tabla
    
    def linkear_tablas(self,link):
        if self.list_dec:                           # Si hay declaraciones.
            self.list_dec.linkear_tablas(link)      #   Les pasamos el link 
        self.list_iden.linkear_tablas(link)         # Le pasamos el link a los identificadores.
        if not isinstance(self.tipo,str):           # Si el tipo es matriz,
            self.tipo.linkear_tablas(link)          #    Pasamos el link al tipo matriz. 
    # Transicion
    def verificar(self,tabla):                  
        if self.list_dec != None:                   # Si hay declaraciones
            self.list_dec.verificar(tabla)          #   Realizar sus verificaciones
        self.list_iden.verificar(tabla)             # Verificaciones de identificadores
        #self.tipo.verificar(tabla)

#############################################################################
#                           TIPO PARA MATRICES                              #
#############################################################################
class cMatriz:
    def __init__(self,dim,tipo,tabla):
        self.type = "Matriz"
        self.dim = dim
        self.tipo = tipo
        self.arr = [self.dim,self.tipo]
        self.tabla = tabla
        self.numDim = 0
        self.tipobase = None
        self.card_dim = 0


    def linkear_tablas(self,link):
        self.dim.linkear_tablas(link)       # Pasamos el link al hijo.
        if not isinstance(self.tipo,str):   # Si el tipo es matriz:
            self.tipo.linkear_tablas(link)  #   Pasamos el link a la matriz hija.
    
    # Transicion:
    #   Como esto solo se usa en lista de declaraciones y alli no se realizan verificaciones,
    #   entonces no es necesario realizar verificaciones adicionales, solo se llaman las veri
    #   ficaciones de los hijos.
    def verificar(self,tabla):
        self.dim.verificar(tabla)           # Verificaciones de lo que tenga dimension.
        if not isinstance(self.tipo,str):   # Si tipo es matriz
            self.tipo.verificar(tabla)      #   Realizamos las verificaciones.

#############################################################################
#                                   DIMENSIONES                             #
#############################################################################
class cDim:                             # ARREGLAR ESTO PARA DIMENSIONES CHEVERONGAS
    def __init__(self,dim,expr):
        self.type = "DIMENSION"     
        self.dim = dim      
        self.expr = expr
        self.arr = [self.dim,self.expr]
        self.numDim = 0
        self.card_dim = 0

    def linkear_tablas(self,link):
        if self.dim:                        # Si hay dimension
            self.dim.linkear_tablas(link)   #   Le pasamos la tabla a la dimension
        self.expr.linkear_tablas(link)      # Le paso el link 

    # Transicion:
    #   Como esto solo se usa en lista de declaraciones y alli no se realizan verificaciones,
    #   entonces no es necesario realizar verificaciones adicionales, solo se llaman las veri
    #   ficaciones de los hijos.
    def verificar(self,tabla):
        self.dim.verificar(tabla)           # Realizamos las verificaciones de la dimension
        self.expr.verificar(tabla)          # Realizamos la verificaciones de la expresion.

#############################################################################
#                           LISTA DE IDENTIFICADORES                        #
#############################################################################
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
    # VERIFICACIONES  
    def verificar(self,tabla):
        # Si tiene lista de identificadores no es vacia.
        if self.lis_iden:    
            self.lis_iden.verificar(tabla)
        if self.expr!="":
            self.expr.verificar(tabla)
            if not isinstance(self.expr.expr,cLitMat):
                if self.expr.tipo != tabla[self.ident]:
                    print("Error de tipo: "+str(self.ident)+" de tipo "\
                    +str(tabla[self.ident])+" pero se le asigno "+str(self.expr.tipo))
                    exit(0)
            else:
                if not (self.expr.tipo.numDim == tabla[self.ident].numDim and \
                    (self.expr.tipo.tipobase==tabla[self.ident].tipobase\
                    or self.expr.tipo.tipobase=="vacio")):
                    print("Error de tipo: "+str(self.ident)+" de tipo Matriz de "\
                        +str(tabla[self.ident].numDim)+" dimensiones y tipo base "\
                        +str(tabla[self.ident].tipobase)+\
                        ", \pero se le asigno Matriz de " + str(self.expr.tipo.numDim)\
                        +" dimensiones y tipo base " + str(self.expr.tipo.tipobase))
                    exit(0)

    def linkear_tablas(self,link):
        if self.lis_iden:
            self.lis_iden.linkear_tablas(link)
        if self.expr!="":
            self.expr.linkear_tablas(link)

#############################################################################
#                           OPERACION DE ASIGNACION                         #
#############################################################################
class cOpasig:
    def __init__(self,expr,tabla):
        self.type = "OPASIG"
        self.expr = expr
        self.arr = [self.expr]
        self.tabla = tabla
        self.tipo = None
    # VERIFICACIONES DE TIPO    
    def verificar(self,tabla):
        self.expr.verificar(tabla)
        if not isinstance(self.expr,cLitMat):
            self.tipo=self.expr.tipo
        else:
            self.tipo = self.expr

    def linkear_tablas(self,link):
        self.expr.linkear_tablas(link)

#############################################################################
#                               INSTRUCCIONES                               #
#############################################################################
class cINST:
    def __init__(self,tipoAux,ident,exp1,exp2,exp3,insgen,tabla,tam):
        self.type = tipoAux
        self.identificador = ident
        self.exp1 = exp1
        self.exp2 = exp2
        self.exp3 = exp3
        self.instgen = insgen
        self.arr = [self.identificador,self.exp1,self.exp2,self.exp3,self.instgen]
        self.tam = tam
        self.tabla = tabla
        self.link = None

    # VERIFICACIONES DE TRANSICION POR CASO
    def verificar(self,tabla):
        if self.tam == 6:
            self.exp3.verificar(tabla)
            self.instgen.verificar(tabla)
        elif self.tam == 10:
            self.exp2.verificar(tabla)
            self.exp3.verificar(tabla)
            self.instgen.verificar(self.tabla)
        else:
            self.exp1.verificar(tabla)
            self.exp2.verificar(tabla)
            self.exp3.verificar(tabla)
            self.instgen.verificar(self.tabla)

    def linkear_tablas(self,link):
        if self.tam >6:
            copia = link.tabla.copy()
            copia[self.identificador] = "iter"
            self.tabla = copia
            self.link = Nodo(link,copia)
            self.instgen.linkear_tablas(self.link)
            if self.exp1:
                self.exp1.linkear_tablas(link)
            if self.exp2:
                self.exp2.linkear_tablas(link)                
            if self.exp3:
                self.exp3.linkear_tablas(link)
        else:
            self.exp3.linkear_tablas(link)
            self.instgen.linkear_tablas(link)

#############################################################################
#                               CONDICIONAL                                 #
#############################################################################
class cCondicional:
    def __init__(self,expr,instgen,auxcond):
        self.type = "CONDICIONAL"
        self.guardia = expr
        self.instgen = instgen
        self.other = auxcond
        self.arr = [self.guardia,self.instgen,self.other]
    
    # VERIFICACIONES        
    def verificar(self,tabla):
        self.guardia.verificar(tabla)
        if self.guardia.tipo!="bool":
            print("Error, guardia de tipo "+self.guardia.tipo+" en lugar de bool.")
            exit(0)
        self.instgen.verificar(tabla)
        if not isinstance(self.other,str):
            self.other.verificar(tabla)

    def linkear_tablas(self,link):
        self.guardia.linkear_tablas(link)
        self.instgen.linkear_tablas(link)
        if not isinstance(self.other,str):
            self.other.linkear_tablas(link)

#############################################################################
#                               ASIGNACIONES                                #
#############################################################################
class cAsig:
    def __init__(self,expr_izq,expr_der): #OJO VERIFICAR BIEN CON LO DE INDEXACION Y MATRICES
        self.type = "ASIGNACION"
        self.expr_izq= expr_izq
        self.expr_der = expr_der
        self.arr = [self.expr_izq,self.expr_der]
    # VERIFICACIONES  
    def verificar(self,tabla):
        self.expr_izq.verificar(tabla)
        self.expr_der.verificar(tabla)
        if not isinstance(self.expr_der,cLitMat):
            if not isinstance(self.expr_izq.tipo,cMatriz):
                if isinstance(self.expr_der.tipo,cMatriz) or isinstance(self.expr_der.tipo,cLitMat): 
                    print("Error, asignando a "+str(self.expr_izq.tipo)+" tipo matriz")
                    exit(0)
                if self.expr_izq.tipo != self.expr_der.tipo or self.expr_izq.tipo=="iter":
                    print("Error, asignando a "+str(self.expr_izq.tipo)+" tipo "+str(self.expr_der.tipo))
                    exit(0)
            else:
                if isinstance(self.expr_der.tipo,cMatriz) or isinstance(self.expr_der.tipo,cLitMat):
                    if self.expr_izq.tipo.numDim!=self.expr_der.tipo.numDim:
                        print("Error, dimensiones y/o de tipo diferentes al asignar")
                        exit(0)
                    else:
                        if isinstance(self.expr_der.tipo,cMatriz):
                            izq = self.expr_izq.tipo
                            der = self.expr_der.tipo
                            while True:
                                if izq.card_dim!=der.card_dim:
                                    print("Error, dimensiones diferentes al asignar")
                                    exit(0)
                                izq = izq.tipo
                                der = der.tipo
                                if izq==None or der==None or isinstance(izq,str) or isinstance(der,str):
                                    break
                        if self.expr_izq.tipo.tipobase!=self.expr_der.tipo.tipobase:
                            print("Error de tipos base en matrices al asignar")
                            exit(0)

                elif self.expr_izq.tipo.tipobase != self.expr_der.tipo:
                    if not (self.expr_izq.tipo.tipobase == "int" and self.expr_der.tipo=="iter"):
                        print("Error, asignando a "+str(self.expr_izq.tipo.tipobase)+" tipo "+str(self.expr_der.tipo))
                        exit(0)                    
        else:
            if not isinstance(self.expr_izq.tipo, cMatriz):
                print("Error asignando literal de matriz a "+self.expr_izq.tipo)
                exit(0)
            else:
                if not(self.expr_izq.tipo.numDim==self.expr_der.numDim and (self.expr_izq.tipo.tipobase==self.expr_der.tipobase\
                    or self.expr_der.tipobase=="vacio")):
                    print(self.expr_izq.tipo.numDim,self.expr_der.numDim)
                    print("EEORROR")
                    exit(0)
    
    def linkear_tablas(self,link):
        self.expr_izq.linkear_tablas(link)
        self.expr_der.linkear_tablas(link)

#############################################################################
#                           INCORPORACION DE ALCANCE                        #
#############################################################################
class cIncAlc:
    def __init__(self,param,tabla):
        self.type = "INCORPORACION DE ALCANCE"
        self.alc = param
        self.arr = [self.alc]
        self.tabla = tabla
        self.link = None
    # Transicion
    def verificar(self,tabla):
        self.alc.verificar()

    def linkear_tablas(self,link):
        self.alc.linkear_tablas(link)

#############################################################################
#                               ENTRADA SALIDA                              #
#############################################################################
class cEntSal:
    def __init__(self,io,expr):
        self.type = "ENTRADA SALIDA"
        self.expr = expr
        self.io = io
        self.arr = [self.expr, self.io]
        self.link = None

    # Verificaciones
    def verificar(self,tabla):
        print("verificando enstal",self.expr)
        self.expr.verificar(tabla)
        if self.io == "read": #INCOMPLETO FALTA INDEXACION
            if  self.expr.type!= "Expresion Unaria":
                exit(0)
            elif not tabla.__contains__(self.expr.expr):
                auxnodo = self.link
                while(auxnodo!=None):
                    if auxnodo.tabla.__contains__(self.expr.expr):
                        self.tipo = auxnodo.tabla[self.expr.expr]
                        break
                    else:
                        auxnodo = auxnodo.padre
                if auxnodo==None:
                    print("Error, "+str(self.expr.expr)+" no fue declarada")
                    exit(0)
        else:
            self.expr.verificar(tabla)

    def linkear_tablas(self,link):
        self.link = link
        self.expr.linkear_tablas(link)

#############################################################################
#                               SECUENCIACION                               #
#############################################################################             
class cSecu:
    def __init__(self,instgen,inst):
        self.type = "SECUENCIACION"
        self.instgen = instgen
        self.inst = inst
        self.arr = [self.instgen,self.inst]
        self.link = None
    # Transicion    
    def verificar(self,tabla):
        self.instgen.verificar(tabla)
        self.inst.verificar(tabla)

    def linkear_tablas(self,link):
        self.instgen.linkear_tablas(link)
        self.inst.linkear_tablas(link)

#############################################################################
#                           EXPRESIONES BINARIAS                            #
#############################################################################
class cExprBin:
    def __init__(self,expr_izq,oper,expr_der,tabla):
        self.type = "Expresion Binaria"
        self.expr_izq = expr_izq
        self.oper = oper
        self.expr_der = expr_der
        self.arr = [self.expr_izq,self.oper,self.expr_der]
        self.tabla = tabla
        self.tipo = None

    # VERIFICACIONES
    def verificar(self,tabla):
        self.expr_izq.verificar(tabla)
        self.expr_der.verificar(tabla)
        if self.oper in {"+","-","*","/","%"}:
            if self.expr_der.tipo == "int" and self.expr_izq.tipo == "int" or (self.expr_der.tipo == "iter" and self.expr_izq.tipo == "int")\
                or (self.expr_der.tipo == "int" and self.expr_izq.tipo == "iter"):
                self.tipo = "int"
            else:
                print("Error de tipo, "+self.expr_izq.tipo+" no es operable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)
        elif self.oper in {"/\\","\\/"}:
            if self.expr_der.tipo == "bool" and self.expr_izq.tipo == "bool":
                self.tipo = "bool"
            else:
                print("Error de tipo, "+self.expr_izq.tipo+" no es operable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)
        elif self.oper in {"<",">","<=",">=","=","/=",}:
            if (self.expr_der.tipo == "int" and self.expr_izq.tipo == "int") or (self.expr_der.tipo == "char" and self.expr_izq.tipo == "char")\
            or (self.expr_der.tipo == "iter" and self.expr_izq.tipo == "int") or (self.expr_der.tipo == "int" and self.expr_izq.tipo == "iter"):
                self.tipo = "bool"
            else:
                print("Error de tipo, "+self.expr_izq.tipo+" no es comparable por "+self.oper+" con "+self.expr_der.tipo)
                exit(0)
        elif self.oper in {"::"}:
            if isinstance(self.expr_der,cLitMat) and isinstance(self.expr_izq,cLitMat):
                if self.expr_der.numDim == self.expr_izq.numDim and  self.expr_der.tipobase == self.expr_izq.tipobase: # Falta caso iter
                    self.tipo = "matriz"


    def linkear_tablas(self,link):
        self.expr_izq.linkear_tablas(link)
        self.expr_der.linkear_tablas(link)

#############################################################################
#                           EXPRESIONES UNARIAS                             #
#############################################################################
class cExprUn:
    def __init__(self,expr,oper,tabla,tam):
        self.type = "Expresion Unaria"
        self.oper = oper
        self.expr = expr
        self.arr = [self.oper, self.expr]
        self.tipo = None
        self.tabla = tabla
        self.tam = tam
        self.link = None

    # VERIFICACIONES
    def verificar(self,tabla):
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
                    #if tabla.__contains__(self.expr):
                    #    self.tipo = tabla[self.expr]
                    #else:
                    auxnodo = self.link
                    while(auxnodo!=None):
                        if auxnodo.tabla.__contains__(self.expr):
                            self.tipo = auxnodo.tabla[self.expr]
                            break
                        else:
                            auxnodo = auxnodo.padre
                    if auxnodo==None:
                        print("Error, "+str(self.expr)+" no fue declarada")
                        exit(0)
            elif isinstance(self.expr,cLitMat):#literal de matriz
                self.tipo = self.expr.tipobase

        # CASO UNARIOS
        elif self.tam == 3:
            self.expr.verificar(tabla)
            if self.oper=="-":
                if self.expr.tipo == "int" or self.expr.tipo == "iter" :
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
            self.expr.verificar(tabla)
            self.tipo = self.expr.tipo

    def linkear_tablas(self,link):
        self.link = link
        if not isinstance(self.expr,str):
            self.expr.linkear_tablas(link)

#############################################################################
#                           LITERALES DE MATRICES                           #
#############################################################################
class cLitMat:
    def __init__(self,auxlitmat):
        self.type = "Literal Matriz"
        self.auxlitmat = auxlitmat
        self.arr = [self.auxlitmat]
        self.numDim = 0
        self.tipobase = "vacio"
        self.link = None

    # VERIFICACIONES DE TIPO
    def verificar(self,tabla):
        if self.auxlitmat:
            self.auxlitmat.verificar(tabla)
            if not (isinstance(self.auxlitmat,cLitMat) or isinstance(self.auxlitmat,cAuxLitMat)):
                self.tipobase = self.auxlitmat.tipo
            else:
                self.tipobase = self.auxlitmat.tipobase

    def linkear_tablas(self,link):
        if self.auxlitmat:
            self.auxlitmat.linkear_tablas(link)

#############################################################################
#                       AUXILIAR LTERALES MATRICES                          #
#############################################################################
class cAuxLitMat:
    def __init__(self,expr,auxlitmat):
        self.type = "AUXLITMAT"
        self.expr = expr
        self.auxlitmat = auxlitmat
        self.arr = [self.expr,self.auxlitmat]
        self.numDim = 0
        self.tipobase = "vacio"
    # VERIFICACIONES
    def verificar(self,tabla):
        self.expr.verificar(tabla)
        self.auxlitmat.verificar(tabla)
        if isinstance(self.expr,cLitMat):
            if isinstance(self.auxlitmat,cLitMat) or isinstance(self.auxlitmat,cAuxLitMat):
                if not(self.expr.numDim==self.auxlitmat.numDim and (self.expr.tipobase==self.auxlitmat.tipobase or self.expr.tipobase=="vacio"\
                    or self.auxlitmat.tipobase=="vacio")):
                    print("EEORROR")
                    exit(0)
            else:
                print("EEORROR no son mismo tipo")
                exit(0)
            
            self.tipobase = self.auxlitmat.tipobase
        else:
            if isinstance(self.auxlitmat,cLitMat) or isinstance(self.auxlitmat,cAuxLitMat):
                print("EEORROR no son mismo tipo")
                exit(0)
            else:
                if self.expr.tipo != self.auxlitmat.tipo:
                    if self.auxlitmat.tipo =="iter" and self.expr.tipo=="int":
                        pass
                    elif self.auxlitmat.tipo =="int" and self.expr.tipo=="iter":
                        pass
                    else:
                        print("Roto")
                        exit(0)
            self.tipobase = self.expr.tipo


    def linkear_tablas(self,link):
        self.expr.linkear_tablas(link)
        self.auxlitmat.linkear_tablas(link)

#############################################################################
#                           INDEXACION DE MATRICES                          #
#############################################################################
class cIndexMat:
    def __init__(self,expr,dim):
        self.type = "Indexacion de Matrices"
        self.mati = expr
        self.indice = dim
        self.arr = [self.mati,self.indice]
        self.tipo = None

    def verificar(self,tabla):
        self.mati.verificar(tabla)
        self.indice.verificar(tabla)
        if isinstance(self.mati,cExprUn) or isinstance(self.mati,cIndexMat):
            if isinstance(self.mati.tipo,cMatriz):
                if isinstance(self.indice,cDim):
                    if self.mati.tipo.card_dim!=self.indice.card_dim:
                        print("Error en las dimensiones al indexar")
                        print(1)
                        exit(0)
                    else:
                        if isinstance(self.mati.tipo.tipo, cMatriz):
                            self.tipo = self.mati.tipo.tipo
                        else:
                            self.tipo = self.mati.tipo.tipo
                else:
                    #print(self.mati.tipo.card_dim,"dim de la var")
                    if self.mati.tipo.card_dim!=1:
                        print("Error en las dimensiones al indexar")
                        print(2)
                        exit(0)
                    else:
                        if isinstance(self.mati.tipo.tipo, cMatriz):
                            self.tipo = self.mati.tipo.tipo
                        else:
                            self.tipo = self.mati.tipo.tipo
                    print("el tipo de la index quedo",self.tipo)
            elif isinstance(self.mati.tipo,cLitMat):
                if isinstance(self.indice,cDim):
                    if self.mati.tipo.numDim<self.indice.card_dim:
                        print("Error en las dimensiones al indexar")
                        print(3)
                        exit(0)
                    elif self.mati.tipo.numDim>self.indice.card_dim:
                        diff = self.indice.card_dim
                        intern_mat = self.mati.tipo
                        while diff!=0:
                            if isinstance(intern_mat.auxlitmat,cAuxLitMat):
                                if isinstance(intern_mat.auxlitmat.expr,cLitMat): #OJO que para la cuarta entrega va a ve cual es
                                    intern_mat = intern_mat.auxlitmat.expr
                                diff -= 1
                            else:
                                if isinstance(intern_mat.auxlitmat,cLitMat): #OJO que para la cuarta entrega va a ve cual es
                                    intern_mat = intern_mat.auxlitmat
                                diff -= 1
                        self.tipo = intern_mat
                    else:
                        self.tipo = self.mati.tipo.tipobase
                else:
                    if self.mati.tipo.numDim!=1:
                        print("Error en las dimensiones al indexar")
                        print(4)
                        exit(0)
                    else:
                        self.tipo = self.mati.tipo.tipobase 
            else:
                print("Error, indexando expresion invalida")
                exit(0)
        elif isinstance(self.mati,cLitMat):
            if isinstance(self.indice,cDim):
                if self.mati.numDim<self.indice.card_dim:
                    print("Error en las dimensiones al indexar")
                    print(5)
                    exit(0)
                elif self.mati.numDim>self.indice.card_dim:
                    diff = self.indice.card_dim
                    intern_mat = self.mati
                    while diff!=0:
                        if isinstance(intern_mat.auxlitmat,cAuxLitMat):
                            if isinstance(intern_mat.auxlitmat.expr,cLitMat): #OJO que para la cuarta entrega va a ve cual es
                                intern_mat = intern_mat.auxlitmat.expr
                            diff -= 1
                        else:
                            if isinstance(intern_mat.auxlitmat,cLitMat): #OJO que para la cuarta entrega va a ve cual es
                                intern_mat = intern_mat.auxlitmat
                            diff -= 1
                    self.tipo = intern_mat
                else:
                    self.tipo = self.mati.tipobase
            else:
                if self.mati.card_dim!=1:
                    print("Error en las dimensiones al indexar")
                    print(6)
                    exit(0)
                else:
                    self.tipo = self.mati.tipobase 
        else:
            print("Error, indexando expresion invalida")
            exit(0)

    def linkear_tablas(self,link):
        self.mati.linkear_tablas(link)
        self.indice.linkear_tablas(link)
