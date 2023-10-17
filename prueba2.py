import random
import json

#tomar tiempo
import time


class Persona(object):
    #grafo de personas familiares
    def __init__(self):
        self._id=None
        self.__familia = None
        self._nombre=None
        self._apellido=None
        self._estado="sano"
        self._probInfeccion = 0
        self.__vacuna = None
        self.__diasInfectado = 0

    def setProbInfeccion(self, prob):
      self._probInfeccion = prob

    def getProbInfeccion(self):
      return self._probInfeccion

    def setEstado(self, estado):
      self._estado = estado

    def getEstado(self):
      return self._estado

    def setFamilia(self, familia):
      self.__familia = familia

    def getFamilia(self):
      return self.__familia

    def setVacunado(self, estado):
      self.__vacuna = estado
    def getVacuna(self):
      return self.__vacuna

    def incrementarDiasInfectado(self):
      if self._estado == "infectado":
        self.__diasInfectado += 1
        if self.__diasInfectado >= 10:
          self._estado = "inmune"



class nodoCola(object):
    info, siguiente =  None, None


class Cola(object):
    def __init__(self):
        self.entrada, self.salida = None, None
        self.tamanio = 0


def arribo(cola, info):
    nuevoNodo = nodoCola()
    nuevoNodo.info = info
    if cola.salida is None:
        cola.salida = nuevoNodo
    else:
        cola.entrada.siguiente = nuevoNodo
    cola.entrada = nuevoNodo
    cola.tamanio += 1



def atencion(cola):
    info = cola.salida.info
    cola.salida = cola.salida.siguiente
    if cola.salida is None:
        cola.entrada = None
    cola.tamanio -= 1
    return info


def ColaEsVacia(cola):
    return cola.entrada is None


def recorrerYVacunar(cola, cantidad):
    colaAuxiliar = Cola()
    contador = cantidad

    while not ColaEsVacia(cola):
        info = atencion(cola)
        if contador >0:
            info.setVacunado(True)
            info.setEstado("inmune")
            contador -= 1
        arribo(colaAuxiliar, info)

    while not ColaEsVacia(colaAuxiliar):
        info = atencion(colaAuxiliar)
        arribo(cola, info)


def arriboColaPrioritaria(cola, info2):
    flag = False
    arriboEspecialFlag = False
    terceraFlag = False
    if ColaEsVacia(cola):
        arribo(cola, info2)
    else:
        colaAuxiliar = Cola()
        while not ColaEsVacia(cola):
            info = atencion(cola)
            if info.getProbInfeccion() <= info2.getProbInfeccion() and flag is False:
                arribo(colaAuxiliar, info2)
                arribo(colaAuxiliar, info)
                flag = True
                terceraFlag = True

            elif info.getProbInfeccion() > info2.getProbInfeccion():
                arribo(colaAuxiliar, info)
                arriboEspecialFlag = True
            elif info.getProbInfeccion() <= info2.getProbInfeccion() and flag is True:
                arribo(colaAuxiliar, info)
            elif info.getProbInfeccion() <= info2.getProbInfeccion() and arriboEspecialFlag is True:
                arribo(colaAuxiliar, info2)
                arribo(colaAuxiliar, info)
                flag = True
                arriboEspecial = False
                terceraFlag = True
        if arriboEspecialFlag is True and terceraFlag is False:
            arribo(colaAuxiliar, info2)
        while not ColaEsVacia(colaAuxiliar):
            info = atencion(colaAuxiliar)
            arribo(cola, info)



def imprimirCola(cola):
    colaAuxiliar = Cola()
    while not ColaEsVacia(cola):
        info = atencion(cola)
        print(info.getProbInfeccion())
        arribo(colaAuxiliar, info)

    while not ColaEsVacia(colaAuxiliar):
        info = atencion(colaAuxiliar)
        arribo(cola, info)

# Nodo simplemente enlazado
class nodoListaSimple(object):
    info, siguiente = None, None


class Lista(object):
    def __init__(self):
        self.inicio = None
        self.tamanio = 0

def insertarLista(lista, info):
    nodo = nodoListaSimple()
    nodo.info = info
    if lista.inicio is None:
        nodo.siguiente = lista.inicio
        lista.inicio = nodo
    else:
        actual = lista.inicio
        siguiente = lista.inicio.siguiente
        while siguiente is not None:
            actual = actual.siguiente
            siguiente = siguiente.siguiente
        nodo.siguiente = siguiente
        actual.siguiente = nodo
    lista.tamanio += 1

def tamanio(lista):
    return lista.tamanio

def eliminar(lista, info):
    data = None
    # saber si es el primero de la lista
    if(lista.inicio.info == info):
        data = lista.inicio
        lista.inicio = lista.inicio.siguiente
        lista.tamanio -= 1
    else:
        actual = lista.inicio
        siguiente = lista.inicio.siguiente
        while (siguiente is not None and info != siguiente.info):
            actual = actual.siguiente
            siguiente = siguiente.siguiente
        # saber si es el ultimo de la lista
        if(siguiente is not None):
            data = siguiente.info
            actual.siguiente = siguiente.siguiente
            lista.tamanio -= 1
    return data

#crea el arbol binari

class Nodo:
    def __init__(self, persona):
        self.persona = persona
        self.izquierda = None
        self.derecha = None

def insertar(nodo, persona):
    if nodo is None:
        return Nodo(persona)
    else:
        if persona._id < nodo.persona._id:
            nodo.izquierda = insertar(nodo.izquierda, persona)
        else:
            nodo.derecha = insertar(nodo.derecha, persona)
    return nodo

def imprimir_inorden(nodo):
    if nodo:
        imprimir_inorden(nodo.izquierda)
        print(f"ID: {nodo.persona._id}, Nombre: {nodo.persona._nombre}, Apellido: {nodo.persona._apellido}, Familia: {nodo.persona.getFamilia()}, Estado de infección: {'Infectado' if nodo.persona.getEstado() == 'infectado' else 'No infectado' if nodo.persona.getEstado() == 'sano' else 'Inmune'}")
        imprimir_inorden(nodo.derecha)
##
def buscar(nodo, id):
    if nodo is None:
        return None
    elif nodo.persona._id == id:
        return nodo
    elif nodo.persona._id < id:
        return buscar(nodo.derecha, id)
    else:
        return buscar(nodo.izquierda, id)

def agrupar_por_familia(nodo):
    familias = {}
    _agrupar_por_familia(nodo, familias)
    return familias

def _agrupar_por_familia(nodo, familias):
    if nodo is None:
        return

    familia = nodo.persona.getFamilia()
    if familia not in familias:
        familias[familia] = []

    estado = 'Infectado' if nodo.persona.getEstado() == 'infectado' else 'No infectado' if nodo.persona.getEstado() == 'sano' else 'Inmune'
    familias[familia].append(estado)

    _agrupar_por_familia(nodo.izquierda, familias)
    _agrupar_por_familia(nodo.derecha, familias)
##
##
def imprimir_por_nivel(raiz):
    pendientes = Cola()
    arribo(pendientes, raiz)
    while(not ColaEsVacia(pendientes)):
        nodo = atencion(pendientes)
        print(f"ID: {nodo.persona._id}, Nombre: {nodo.persona._nombre}, Apellido: {nodo.persona._apellido}, Familia: {nodo.persona.getFamilia()}, Estado de infección: {'Infectado' if nodo.persona.getEstado() == 'infectado' else 'No infectado' if nodo.persona.getEstado() == 'sano' else 'Inmune'}")
        if(nodo.izquierda is not None):
            arribo(pendientes,nodo.izquierda)
        if(nodo.derecha is not None):
            arribo(pendientes, nodo.derecha)


def start():
    #ARCHIVO CON INFORMACIO PARA LLENADO
    with open("datosnombres.json", "r") as f:
        data = json.load(f)

    nombres = data["nombres"]
    apellidos = data["apellidos"]

    lista_personas= Lista()

    #crea a mil objetos y los inserta a lista

    for i in range(1, 1001):
        persona= Persona()
        persona._id= i
        persona._nombre= random.choice(nombres)
        persona._apellido= random.choice(apellidos)
        persona.setFamilia(random.randint(1,10))

        if random.random() < (random.randint(1,10) / 100.0):
          persona.setEstado("infectado")

        insertarLista(lista_personas, persona)

    #SIMULACION
    for dia in range(30):
        actual= lista_personas.inicio
        while actual is not None:
            persona= actual.info

            if persona.getEstado() != "sano":
                persona.incrementarDiasInfectado()
                actual= actual.siguiente
                continue

            miembros_familia_infectados= 0
            miembros_familia_total= 0
            temp= lista_personas.inicio

            while temp is not None:
                p_temp= temp.info

                if p_temp.getFamilia() == persona.getFamilia():
                    miembros_familia_total+= 1

                    if p_temp.getEstado() == "infectado":
                        miembros_familia_infectados+= 1

                temp= temp.siguiente


            #INFECCION PROBABILIDAD Y AUMENT SI ESTA EN UNA FAMILIA
            probAzar = random.randint(0, 10000000) / 10000000
            probEnfermo = random.randint(0, 10000000) /10000000
            """
            #prob_infeccion= 0.1
            if miembros_familia_infectados > miembros_familia_total / 2:
                prob_infeccion*= 4
            elif miembros_familia_infectados > 0:
                prob_infeccion*= 2
            persona.setProbInfeccion(prob_infeccion)
            if random.random() < prob_infeccion:
                persona.setEstado("infectado")
            """
            if miembros_familia_infectados > miembros_familia_total / 2:
                probAzar += 0.04
            elif miembros_familia_infectados > 0:
                probAzar += 0.01
            persona.setProbInfeccion(probAzar)
            if probEnfermo < probAzar:
                persona.setEstado("infectado")

            actual= actual.siguiente

        total_infectados= 0
        total_no_infectados= 0
        total_inmunes= 0

        actual= lista_personas.inicio
        #cola y cola prioridad
        colaPrioritaria = Cola()

        while actual is not None:
            persona = actual.info
            """

                cola = Cola()
                persona = Persona()
                persona2 = Persona()
                persona3 = Persona()
                persona4 = Persona()

                arribo(cola, persona)
                arribo(cola, persona2)
                arribo(cola, persona3)
                arribo(cola, persona4)

                recorrerEInfectar(cola)



                colaPrioritaria = Cola()
                arriboColaPrioritaria(colaPrioritaria, persona)
                print("\n--------\n")
                arriboColaPrioritaria(colaPrioritaria, persona2)
                print("\n--------\n")
                arriboColaPrioritaria(colaPrioritaria, persona3)
                arriboColaPrioritaria(colaPrioritaria, persona4)

                print("-----despues de cola prioritaria, colaPrioritaria:", colaPrioritaria.tamanio)
                imprimirCola(colaPrioritaria)
            """
            #funciona pero aumenta la ram ocupada
            if persona.getEstado() is "sano":
                arriboColaPrioritaria(colaPrioritaria, persona)
            #print("Persona:", persona._id, " Tiene la prob", persona.getProbInfeccion())
            actual = actual.siguiente
        #recorre la cola y vacuna a 5
        recorrerYVacunar(colaPrioritaria, 5)
        actual= lista_personas.inicio

        while actual is not None:
            persona= actual.info

            if persona.getEstado() == "infectado":
                total_infectados+= 1
            elif persona.getEstado() == "sano":
                total_no_infectados+= 1
            else:
                total_inmunes+= 1

            actual= actual.siguiente

        print(f"Día {dia+1}: Total infectados: {total_infectados}, Total no infectados: {total_no_infectados}, Total inmunes: {total_inmunes}")


    lista_personas_array = []
    actual = lista_personas.inicio
    while actual is not None:
        lista_personas_array.append(actual.info)
        actual = actual.siguiente


    personas_seleccionadas = random.sample(lista_personas_array, 300)


    for persona in personas_seleccionadas:
        print(f"ID: {persona._id}, Nombre: {persona._nombre}, Apellido: {persona._apellido}, Familia: {persona.getFamilia()}, Estado de infección: {'Infectado' if persona.getEstado() == 'infectado' else 'No infectado' if persona.getEstado() == 'sano' else 'Inmune'}")

    raiz = None
    for persona in personas_seleccionadas:
        raiz = insertar(raiz, persona)

    print("Árbol binario en orden:")
    imprimir_inorden(raiz)

    BUSCAR=input("¿Que filtro nesecesita ingresar a la tabla? (id,familia)")
    if BUSCAR=="id":
        id_buscar = int(input("Por favor, ingresa el ID que deseas buscar: "))
        inicio = time.time()
        nodo_encontrado = buscar(raiz, id_buscar)
        fin = time.time()
        print(f"El tiempo de ejecución fue: {fin - inicio} segundos")
    elif BUSCAR=="familia":
        #familia_buscar=int(input("Por favor, ingresar el grupo familiar que deseas buscar: "))
        #nodo_encontrado=buscar(raiz, familia_buscar)
        pass
    if nodo_encontrado is not None:
        print(f"Se encontró a la persona con ID: {nodo_encontrado.persona._id}, Nombre: {nodo_encontrado.persona._nombre}, Apellido: {nodo_encontrado.persona._apellido}, Familia: {nodo_encontrado.persona.getFamilia()}, Estado de infección: {'Infectado' if nodo_encontrado.persona.getEstado() == 'infectado' else 'No infectado' if nodo_encontrado.persona.getEstado() == 'sano' else 'Inmune'}")
    else:
        print("No se encontró a ninguna persona con ese ID.")

    # busqueda a travez del tiempo para hacer pruebas
    id_buscar = int(input("Por favor, ingresa el ID que deseas buscar: "))
    inicio = time.time()
    nodo_encontrado = buscar(raiz, id_buscar)
    fin = time.time()
    a=fin - inicio
    print(f"El tiempo de ejecución de la búsqueda en el árbol binario fue: {a} segundos")

    inicio = time.time()
    persona_encontrada = None
    for persona in (lista_personas_array):
        if persona._id == id_buscar:
            persona_encontrada = persona
            break
    fin = time.time()
    b=(fin - inicio)
    print(f"El tiempo de ejecución de la búsqueda en la lista fue: {b} segundos")
    if a <b:
        print("lista mas grande")

start()