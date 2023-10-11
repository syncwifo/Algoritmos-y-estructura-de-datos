import random
import json

#ARCHIVO CON INFORMACIO PARA LLENADO
with open("datosnombres.json", "r") as f:
    data = json.load(f)

nombres = data["nombres"]
apellidos = data["apellidos"]

class Persona(object):
    #grafo de personas familiares
    def __init__(self):
        self._id=None
        self.__familia = None
        self._nombre=None
        self._apellido=None
        self._estado="sano"  
        self.__vacuna = None
        self.__diasInfectado = 0

    def setEstado(self, estado):
      self._estado = estado

    def getEstado(self):
      return self._estado

    def setFamilia(self, familia):
      self.__familia = familia

    def getFamilia(self):
      return self.__familia

    def incrementarDiasInfectado(self):
      if self._estado == "infectado":
        self.__diasInfectado += 1
        if self.__diasInfectado >= 10: 
          self._estado = "inmune"

# Nodo simplemente enlazado
class nodoListaSimple(object):
    info, siguiente = None, None


class Lista(object):
    def __init__(self):
        self.inicio = None
        self.tamanio = 0

def insertar(lista, info):
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

# from lista import Lista, insertar, imprimir, tamanio, eliminar

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
    
    insertar(lista_personas, persona)

#SIMULACION 
for dia in range(100): 
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
        prob_infeccion= 0.1  
        if miembros_familia_infectados > miembros_familia_total / 2:
            prob_infeccion*= 4 
        elif miembros_familia_infectados > 0:
            prob_infeccion*= 2 
        if random.random() < prob_infeccion:
            persona.setEstado("infectado")
        actual= actual.siguiente

    total_infectados= 0 
    total_no_infectados= 0 
    total_inmunes= 0 
    
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
