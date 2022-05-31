#Compilador de una versión recortada de lenguaje “C”
#inicializar variables (parte de analisis semantico)
class Variables:  
    nombre =""      
    tipo =""
    valor =""
    direccion=0
    def __init__(self,n,t,v,d):  #self- como el this de java
        self.nombre =n
        self.tipo =t
        self.valor =v
        self.direccion =d     

def esOperador(v):
    return (v in "*/+-")

class Pila:
    arreglo = []
    def meter(self, dato):
        self.arreglo.append(dato)
    def sacar(self):
        if (len(self.arreglo)==0):
            print("Pila vacia")
        else:
            return self.arreglo.pop()

#separa tokens
def esSeparador(carac): #para saber si es separador (caracter)
    return carac in " \n\t" #si tiene espacio o salto de linea es separador

def esSimboloEsp(carac): #para saber si es caracter especial
    return carac in "()[]{}:=+-*;,.:!=<><=>=%&/"

def tokeniza(cad):                  #lo mismo que el visto en clase, se unen las funciones anteriores, separa cada espacio,palabra
    tokens = []                     #arreglo
    dentro = False                  
    token = ""                      #declarar token(palabra)
    for c in cad:                   #c recorrriendo nuestra cad(dena)
        if dentro:                  #esta dentro del token
            if esSeparador(c):      #si parametro "c" es separador entonces:
                tokens.append(token)#agregar a "tokens" cada token que pase por "token" XD
                token = ""          #reiniciar "token"
                dentro = False      #salir de if
            elif esSimboloEsp(c):   #si parametro "c" es simbolo especial entonces:
                tokens.append(token)#agregar a "tokens" cada token que pase por "token" XD
                tokens.append(c)    #agregar token simbolo especial, dentro del token
                token = ""
                dentro = False
            else:
                token = token + c
        else:                       #esta fuera del token ()
            if esSimboloEsp(c):     #simbolo espcial fuera del token (la mayoria son ;)
                tokens.append(c)    #agregarlo a tokens
                #print("esta fuera del toqueeeen",c)
            elif esSeparador(c):
                a=0
            else:
                dentro = True
                token = c
    if token != '': 
       tokens.append(token)
    return tokens

#primero se le deben quitar los comentarios 
def quitaComentarios(cad):                                                                                      #QUITA_COMMENTS___
    estado ="Z"                      #estado inicial = Z, iremos encontrando los caracteres "/**/" 
    cad2 =""                         #en cad2 almacenamos todo aquello fuera de "/**/"
    for c in cad:                    #recorremos parametro "cad" en nuestra variable "c" 
        if (estado=="Z"):
            if (c=="/"):             #si encontramos un "/" inicial de un comentario en #C
                estado = "A"         #pasamos al estado A --- a buscar la segunda parte "*"
            else:                    #de lo contrario cad2 le almacenamos cad2 + c 
                cad2 = cad2 + c      
        elif (estado=="A"):          #estado "A" --> abriendo un comentario "/*"
            if (c=="*"):             #así vamos omitiendo todo lo que se encuentre dentro de
                estado="B"           #los caracteres especiales para comentarios en C
            else:                    #DE lo contrario no siga un "*" tenemos otra cosa que no
                estado = "Z"         #es un comentario, entonces agregamos el "/" que se omitio 
                cad2=cad2+"/"+c      #en el estado "Z"
        elif (estado=="B"):          
            if (c=="*"):             
                estado = "C"         
        elif(estado=="C"):           #estado "C" --> cerrando un comentario "*/"
            if (c=="/"):
                estado="Z"
            else:
                estado="B"           #en dado caso retornaramos "cad" veriamos el prog 
    return cad2                      #con todo y comentarios


#crear una tabla de variables donde se almacene cada variable como se muestra en el PDF                            ##TABLAAAAA

def estaEn_LaTabla(nombreD_Variable): #saber si la variable ya esta en la tabla
    siEsta = False
    for v in tablaVariables:
        if(v.nombre == nombreD_Variable):    #si los nombres son iguales entonces "siEsta"=cierto
            siEsta = True
    return siEsta


def agregarVariable(dato,direcc):                                                                   
    tipos=["int","string","char","float"] # tipos de datos que se van a considerar para la tabla
    datos = dato.split()                   #split para separar por ()espacios un string (datos) 
    nombreD_Variable = datos[2][:-1]      #[:-1] todo menos el ultimo string
    tipoD_Variable = datos[1]
    if tipoD_Variable in tipos:           #recorrer para comparar los nombres de las variables
        if estaEn_LaTabla(nombreD_Variable): #encontrar variable que ya se encuentre en la tabla
            print(f"VARIABLE DECLARADA ANTERIORMENTE ---> {nombreD_Variable} \n")               ######################solo di formato
            quit()                          #interrumpir cuando una variable sea redeclarada    #ERROR VAR_REDECLARADA__
        else:                               #de lo contrario la agregamos a la tabla
            tablaVariables.append(Variables(nombreD_Variable, tipoD_Variable, "0.0",direcc))
    else:
        print("Tipo de dato enexistente:", tipoD_Variable )
    pass


def imprimeTabla():                                                                       #yo
    print("\n \t NOMBRE     TIPO     VALOR     DIRECCIÓN ")     #formato de la tabla
    for v in tablaVariables:                    #recorrer la tabla de variables para imprimirlas
        print("  \t  ",v.nombre,"\t  ",v.tipo,"    ",v.valor,"\t ",v.direccion)
    pass

def obtenerPrioridadOperador(o): # Función que trabaja con convertirInfijaA**.
    return {'(':1, ')':2, '+': 3, '-': 3, '*': 4, '/':4, '^':5}.get(o)

def convertirInfijaAPostfija(infija):
    '''Convierte una expresión infija a una posfija, devolviendo una lista.'''
    pila = []
    salida = []
    for e in infija:
        if e == '(':
            pila.append(e)
        elif e == ')':
            while pila[len(pila) - 1 ] != '(':
                salida.append(pila.pop())
            pila.pop()
        elif e in ['+', '-', '*', '/', '^']:
            while (len(pila) != 0) and (obtenerPrioridadOperador(e)) <= obtenerPrioridadOperador(pila[len(pila) - 1]):
                salida.append(pila.pop())
            pila.append(e)
        else:
            salida.append(e)
    while len(pila) != 0:
        salida.append(pila.pop())
    
    return salida

def esId(cad):
    return (cad[0] in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

#_____________________________________________________________________________________________________________________________________

'''
def codigoIntermedio(opPostfija):       #debe trabajar con la operaion en postfija
    print("\n CODIGO INTERMEDIO")
    #t1=[]
    t="T"
    contVar=0
    t2=[]                               #operadores
    t3=[]                               #variables
    anteValor=""                        #valor anterior de t3
    ite=0                               #iterador para contar posiciones
    ite2=0
    operacion=[]                        #op final
    temp=opPostfija
    operacionFinal=[]
    for op in temp:
        #t1=temp   va guardando op en una lista
        
        if esOperador(op):          #if para saber si es operador
            t2.append(op)           #va guardando cada que op es operador
            contVar+=1
            #print("\n t1 es: ",t1," y t2 es: ",t2,"TE3: ",t3)
            if op=="+":         #if's para separar operadores de las variables
                if anteValor==t3[-1]:
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t+str(contVar-2)+"+"+t+str(contVar-1) #operacion+"T"+str(contVar-1)+"+"+t3[-3]
                    t3.append(operacion[0:2])       #se agrega variable a t3
                    ite+=1
                    #print(operacion)
                else:
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t3[-2]
                    operacion=operacion+op
                    operacion=operacion+t3[ite-1]
                    #print(operacion)
                
            elif op=="-":
                if anteValor==t3[-1]:   #antepenultimo valor de t3, es igual signifca que tenemos la misma variable repetida
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t+str(contVar-2)+"-"+t+str(contVar-1) #operacion+"T"+str(contVar-1)+"-"+t3[-3]
                    t3.append(operacion[0:2])       #se agrega variable a t3
                    ite+=1
                    #operacion=operacion+"T"+str(contVar-1)+"-"+"T"+str(contVar-2)
                    #print(operacion)
                #print("no entro porque", anteValor, t3[-1])
                else:
                    operacion=t+str(contVar)+" = "  #t="T" contVar="1,2,3..." + " = " ---> " T1 = "
                    operacion=operacion+t3[-2]      #t3 en la posicion ante penultima, por si llega haber mas de 2 var (abc+)
                    operacion=operacion+op          #el operador en medio de las dos var
                    operacion=operacion+t3[ite-1]   #la ultima var será "ite-1" porque operacion tiene elemento en posicion [0]
                    #print(operacion)
                
            elif op=="*":
                if anteValor==t3[-1]:   
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t+str(contVar-2)+"*"+t+str(contVar-1)   #t3[-3] 
                    t3.append(operacion[0:2])       #se agrega variable a t3
                    ite+=1                          #se aumenta a ite que controla el num de variables
                    #print(operacion)
                else:
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t3[-2]
                    operacion=operacion+op
                    operacion=operacion+t3[ite-1]
                    #print(operacion)
                
            elif op=="/":
                if anteValor==t3[-1]:   #
                    #print("SI deberia entrar porque: ", t3[-1],anteValor)
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t+str(contVar-2)+"/"+t+str(contVar-1) #+t3[-3] 
                    t3.append(operacion[0:2])       #se agrega variable a t3
                    ite+=1                          #se aumenta a ite que controla el num de variables
                    #print(operacion)
                else:
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t3[-2]
                    operacion=operacion+op
                    operacion=operacion+t3[ite-1]
                    #print(operacion)
                
            elif op=="^":
                if anteValor==t3[-1]:   #
                    #print("SI deberia entrar porque: ", t3[-1],anteValor)
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t+str(contVar-2)+"^"+t+str(contVar-1)   #operacion+"T"+str(contVar-1)+"^"+t3[-3]
                    t3.append(operacion[0:2])       #se agrega variable a t3
                    ite+=1                          #se aumenta a ite que controla el num de variables
                    #print(operacion)
                else:
                    operacion=t+str(contVar)+" = "
                    operacion=operacion+t3[-2]
                    operacion=operacion+op
                    operacion=operacion+t3[ite-1]
                    #print(operacion)
            operacionFinal.append(operacion)
            anteValor=t3[-1]                 #asignar el ultimo valor de t3 a anteValor
            #print("esto vale t3",t3,t2)
        else:
            t3.append(op)       #t3 va guardando todo las variables
            ite+=1              #contador para saber la cada que se agrega una variable y asu vez su POSICION
        #print("ope",operacionFinal)
    return operacionFinal
'''


#sustituir print y read por interrupciones y guardar en la direccion correspondiente según la tabla

def sustInterrupcion(dato):  
    datos=tokeniza(dato)
    datos2 =""
    conta=0
    for c in datos:                   #recorrer cadena
        if(datos[0]!="var"):                     ##quitar declaracion de variables, siempre que los datos sean diferente de "var"
            if (c=="read"):             #encontrar read
                for n in datos:           #
                    if estaEn_LaTabla(n):   #si esta en tabla entramos       
                        for v in tablaVariables:          #recorrer tablaVar que tiene el tipo de dato
                            if (v.nombre == n):     #si n == v.nombre
                                if v.tipo == "int": #encontrar cual es y sustituir según corresponda la interrupción
                                    c="IN1"
                                elif v.tipo == "float":
                                    c="IN2"
                                elif v.tipo == "char":
                                    c="IN3"
                                elif v.tipo == "string":
                                    c="IN4"
            elif (c=="print"):          #encontrar print
                if ("," in datos):      #si hay "," es porque debe de haber una variable despues de
                    for a in datos:
                        #print("esto vale datos en cont=0",datos)
                        conta+=1           #
                        if (datos[conta-1]==","): #
                            #print("esto vale datos en cont=1",datos)
                            if estaEn_LaTabla(datos[conta]):   #si encontramos dato en "estaEn_LaTabla"
                                for v in tablaVariables:    #
                                    if (v.nombre == datos[conta]): #si el nombre de la Var coincide con datos 
                                        if v.tipo == "int":     #buscamos el tipo
                                            c="IN5"
                                        elif v.tipo == "float":
                                            c="IN6"
                                        elif v.tipo == "char":
                                            c="IN7"
                                        elif v.tipo == "string":
                                            c="IN8"           
                else:
                    c="IN9"                 #si no hay tipo de variable, es solo una cadena "IN9"

            elif (c=="println"):            #lo mismo que pal print pero con println (con salto)
                if ("," in datos):          #mismas instrucciones que con print
                    for a in datos:
                        conta+=1
                        if (datos[conta-1]==","):
                            if estaEn_LaTabla(datos[conta]):
                                for v in tablaVariables:
                                    if (v.nombre == datos[conta]):
                                        if v.tipo == "int":     #buscamos el tipo
                                            c="IN5"
                                        elif v.tipo == "float":
                                            c="IN6"
                                        elif v.tipo == "char":
                                            c="IN7"
                                        elif v.tipo == "string":
                                            c="IN8"         
                else:
                    c="IN9s"

            datos2 = datos2 + "" + c   #CONCATENAMOS LA INTERRUPCION CON EL STRING CORRESPONDIENTE 
    return datos2

def obtenerOp(datos):               #detecta cuando hay una operación y la separa apartir del "=" ---> (y2 - y1) / (x2 - x1)
    cad2 = quitaComentarios(datos)
    cad2=tokeniza(datos)            #pa seprar en lista
    op=[]                           #pa guardar la lista
    it=0                            #contador con valor en 0
    for temp in cad2:               #recorremos cad2
        it+=1                       #aumentamos en 1 cada vez que a temp se le de un valor de cad2
        if(temp=="=" and cad2[-1]==";"):    #si temp es "=" y cad2 en la ultima pos =  ";" (siempre)
            op= op+ cad2[it:-1]     #op toma valor de la pos del iterador (it) cuando temp valio es "=" hasta la pos
            #print("TEMPPP",temp)    #penultima en la lista de cad2, o sea uno antes del ";"
            print("operacion encontrada: ",op)    #(y2 - y1) / (x2 - x1)
    return op

def obtenerOpCompleta(datos):       #detecta la ope y la almacena completa  ------> m = ( y2 - y1 ) / ( x2 - x1 ); 
    cad2 = quitaComentarios(datos)
    cad2=tokeniza(datos)            #pa seprar en lista
    opCompleta=""                           #pa guardar la operacion
    it=0                            #contador con valor en 0
    for temp in cad2:               #recorremos cad2
        it+=1                       #aumentamos en 1 cada vez que a temp se le de un valor de cad2
        if(temp=="=" and cad2[-1]==";"):    #si temp es "=" y cad2 en la ultima pos =  ";" (siempre)
            opCompleta= "".join(cad2[:])      #join une los elementos de una lista, en este caso sin separacion "" (eliminara los espacios) 
            #para poder comparar en la funcion codigoEnsa. OpCompleta cad2[:] ---> todo cad2 m=(y2-y1)/(x2-x1); 
            #print("TEMPPP",temp)             #penultima en la lista de cad2, o sea uno antes del ";"
    return opCompleta                 #m = (y2 - y1) / (x2 - x1);

def codigoIntermedio(datos,opCompleta):    #detecta CUALQUIER variable total como "m" (datos, opCompleta='t1=y2-y1;','t2=x2-x1;','t3=t1/t2;')
    op=""
    cad2 = quitaComentarios(datos)
    cad2 =tokeniza(datos)
    operacionFinal=opCompleta[-1]   #operacionFinal=";" t3=t1/t2;
    it=0                            #contador con valor en 0
    for temp in cad2:               #recorremos cad2
        it+=1                       #aumentamos en 1 cada vuelta
        if(temp=="=" and cad2[-1]==";"):    #si temp es "=" y cad2 en la ultima pos =  ";" (siempre) cad2---> m=(y2-y1)/(x2-x1);
            op=op+" ".join(cad2[0:it-1])        #guarda la lista [del primero:hasta it-1] --->  "m"
            op=op+str(operacionFinal[it:])    # op ----> "m" + "=t1/t2;" <----- operacionFinal m=t1/t2
    return op
'''
def codigoIntermedio(vartotal,intermedioSinVar):
    cont=0
    ultimaOperacion=intermedioSinVar[-1]
    print("ultima operaiones",ultimaOperacion)    #t3=t2/t1
    for i in ultimaOperacion:
      cont+=1
      if i == "=":                                  
        codIntermedioFinal=vartotal+ultimaOperacion[cont:]  #m=t1/t2;
        print("essssss",codIntermedioFinal)     #ssssss m = mt1/t2;
'''

def esSinCosTan(cad):                                   #saber si cad es igual a sin cos tan
    Trigonometricas = "sin cos tan"
    return cad in Trigonometricas                       #regresamos el valor según sea

def codigoEnsa(postfija):
    posfija=postfija
    ct = 1
    pila1 = Pila()
    intermedio = []
    codigo = []
    codigoEnsamblador=[]
    archivo = open("ProPrueba_1.txt", "r") #ahora el prog, pero con interrupciones
    for dat2 in archivo:
      datos = quitaComentarios(dat2)
      datos2=tokeniza(datos)
      opeCompleta=obtenerOpCompleta(dat2)           #opCompleta ---> m=(y2-y1)/(x2-x1)
      datosSinEspacios=datos[0:-1].replace(" ", "") #replace es para eliminar espacios y es de 0 a -1 por salto de linea que daba y no entraba al if de abajo
      if datosSinEspacios==opeCompleta:      # solo entrar cuando eontremos a m=(y2-y1)/(x2-x1) == m=(y2-y1)/(x2-x1) para generar el codigo intermedio en ORDEN
        for e in posfija:                     #
            if esOperador(e):
                op2 = pila1.sacar()
                op1 = pila1.sacar()
                cad = "t"+str(ct)+"="+op1+e+op2+";"
                intermedio.append(cad)
                #print("LDA "+op1+";")
                codigoEnsamblador.append("LDA "+op1+";")
                if e=="+":
                    #print("ADD "+op2+";")
                    codigoEnsamblador.append("ADD "+op2+";")
                elif e=="*":
                    #print("MUL "+op2+";") 
                    codigoEnsamblador.append("MUL "+op2+";") 
                elif e=="-":
                    #print("SUB "+op2+";")
                    codigoEnsamblador.append("SUB "+op2+";")
                elif e=="/":
                    #print("DIV "+op2+";")
                    codigoEnsamblador.append("DIV "+op2+";")
                pila1.meter("t"+str(ct))
                #print("STA "+ "t"+str(ct)+";")
                codigoEnsamblador.append("STA "+ "t"+str(ct)+";")
                ct = ct + 1
            else:
                pila1.meter(e)
        codigoInter=codigoIntermedio(dat2,intermedio) #sacar codigo intermedio codigoInter= m=t1/t2;
      
      elif esSinCosTan(datos2[0]):                            #si cad2 en [0] esSIN,COS,TAN        
        codigoEnsamblador.append(datos2[0].upper()+" "+datos2[2]+";") #mayusculas a datos2[0](SIN, COS, TAN) + datos2[2] (y1,y2,x1...)
        codigoEnsamblador.append("STA "+datos2[2]+";")     ###         

      elif (datos2[1] != "=" and datos2[-1]==";" and datos2[0]!="end"):    #todo aquello que no sea end y la operacion de m=(y2-y1)...  
        sustituir= sustInterrupcion(datos)
        codigoEnsamblador.append(sustInterrupcion(datos))

    print("\nEste es el codigo intermedio: \n")
    for i in intermedio:      #for para darle formato a la impresion jaja
      print(i)

    intermedio[-1]=codigoInter                #t3=t1/t2; ----> m=t1/t2;

    print("\nEste es el codigo intermedio con ultima var en la ultima operacion: \n")
    for j in intermedio:      ##
      print(j)
    return codigoEnsamblador
  


#____________________________________________________________________________________________________________________________

#ARROJAMOS DATOS ------- LLAMADO DE FUNCIONES

archivo = open("ProPrueba_1.txt", "r") #abrimos archivo en read

direccion=500
tablaVariables = []
conta=1;

print("Eliminando comentarios")
for dat in archivo:
    datos = quitaComentarios(dat)                      #pasamos la funcion que quita comentarios
    print(datos)                                       #imprimimos sin comentarios
    temp = tokeniza(datos)
    if(temp[-1]==";"):                                 ###########ERROR, si no hay ";" en el programa
      if(temp[0]=="var"):
          agregarVariable(datos,direccion)
          direccion+=1
      if(temp[0]=="end"):                 #esperar a que print(datos)llegue al fin, para imprimir ahora
          archivo = open("ProPrueba_1.txt", "r") #ahora el prog, pero con interrupciones
          print("\nPROCESAR LAS VARIABLES Y REMPLAZAR 'print' y 'read' por INTERRUPCIONES\n")
          for dat2 in archivo:
              datos2 = quitaComentarios(dat2)    
              interrupcion= sustInterrupcion(datos2)
              print(interrupcion)                                
    else:
        print("ERROR, FALTA UN PUNTO Y COMA EN ---> ", datos)
        exit()

print("\n TABLA DE VARIABLES")
imprimeTabla()





archivo = open("ProPrueba_1.txt", "r")          #CONVERTIR E IMPRIMIR POSTFIJA
print("\n ENCONTRAR OPERACION Y CONVERTIRLA A POSTFIJA\n")
codi=[]
for dat2 in archivo:
    datos2 = quitaComentarios(dat2)                           #si la operacion no tiene valor, decir no a encontrado una ope
    operacion=obtenerOp(dat2)
    if (operacion!=[]):                         #entonces no convertimos ni imprimimos nada, DE LO CONTRARIO
        operacionPost=convertirInfijaAPostfija(operacion)
        print("operacion convertida a postfija: ",operacionPost)
        print("\n Codigo Intermedio y Ensamblador: ")
        ensamblador=codigoEnsa(operacionPost)
        for i in ensamblador:
          print(i)
archivo.close()

def codigoEnsaFor(postfija):                ##mismo de arriba solo sin sen,cos,tan
    posfija=postfija
    ct = 1
    pila1 = Pila()
    intermedio = []
    codigo = []
    codigoEnsamblador=[]                    
    for e in posfija:    
        if esOperador(e):
            op2 = pila1.sacar()
            op1 = pila1.sacar()
            cad = "t"+str(ct)+"="+op1+e+op2+";"
            intermedio.append(cad)
            #print("LDA "+op1+";")
            codigoEnsamblador.append("LDA "+op1+";")
            if e=="+":
                #print("ADD "+op2+";")
                codigoEnsamblador.append("ADD "+op2+";")
            elif e=="*":
                #print("MUL "+op2+";") 
                codigoEnsamblador.append("MUL "+op2+";") 
            elif e=="-":
                #print("SUB "+op2+";")
                codigoEnsamblador.append("SUB "+op2+";")
            elif e=="/":
                #print("DIV "+op2+";")
                codigoEnsamblador.append("DIV "+op2+";")
            pila1.meter("t"+str(ct))
            #print("STA "+ "t"+str(ct)+";")
            codigoEnsamblador.append("STA "+ "t"+str(ct)+";")
            ct = ct + 1
        else:
            pila1.meter(e)
    return codigoEnsamblador


archivo = open("progFor.txt", "r") 
ensambladorFor=[]
valoresVar=[]
cont=1
dentroFor=0
for dat2 in archivo:
  datos = quitaComentarios(dat2)
  datos2=tokeniza(datos)
  if datos[0]!="{" and datos[0]!="}":       #tira error por la posicion de cad[1] cuando en "{" no hay posicion [1] 
    if dentroFor!=1:                      #si ya se entro al bucle for no volver a carga "a=a*b"
      if datos2[1]=="=":                  #_fin y a = a    *2
        ensambladorFor.append("LDV "+datos2[2]+";")      #LDV 5 y 2
        ensambladorFor.append("STA "+datos2[0]+";")      #STA _fin y b
        valoresVar.append(int(datos2[2]))                     #agregar a valoresVar el valor seguido del "=" (_fin=5)
                                                        #valoresVar[0]=5                                                
    if datos2[0]=="for":              #dentro del for
      for i in range(0,8):            ##recorrer datos[] dentro del for. rango (0-7) 
        if datos2[i]=="=":                    #c=1
          ensambladorFor.append("LDV "+datos2[i+1]+"; ")   #LDV 1
          ensambladorFor.append("STA "+datos2[i-1]+";")    #STA c
          valoresVar.append(int(datos2[i+1]))              #agregar a valoresVar el valor seguido del "=" (c=1)
                                                      #valoresVar[1]=1
        elif datos2[i]==";":                            #";" dentro del for   
          ensambladorFor.append("LDA "+datos2[i-3]+";")  #LDA c
          ensambladorFor.append("SUB "+datos2[i+1]+";")  #SUB _fin
    
        elif datos2[i]==")":
          dentroFor=1                           #ya se entro al for, dentroFor=1 YYY pasamos el c=1

    if datos2[1]=="=" and dentroFor==1:   #dentro del bucle. datos2[1] = "=" (a = a * b)
      ensambladorFor.append("JZ #2;")     #si c==5 o c>5 saltamos a la etiqueta 2
      if valoresVar[2]<valoresVar[1]:                   #1<5 c<_fin
        operacion=obtenerOp(datos2)
        operacionPost=convertirInfijaAPostfija(operacion)
        print("esto es la operacion posfija",operacionPost)
        agrega=codigoEnsaFor(operacionPost)                      #agrega=['LDA a;', 'MUL b;', 'STA t1;']
        for temp in agrega:                                    #para esto el for
          ensambladorFor.append(temp)                          #de uno en uno en "ensambladorFor"
        #valoresVar[2]+=1
        ensambladorFor.append("JMP #1;")
      else:     #etiqueta #2.    cuando c==5 o c>5
        print()#knkgfm
    elif datos2[0]=="end":
      ensambladorFor.append("END;")

for i in ensambladorFor:
    print(cont,i)
    cont+=1

for k in valoresVar:
    print(k)
