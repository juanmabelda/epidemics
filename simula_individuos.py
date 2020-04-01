# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 09:37:08 2020

@author: jmbelda
"""

import matplotlib.pyplot as plt
from numpy import pi, cos, sin, array, round
from numpy.linalg import norm
from numpy.random import rand, randint


plt.rcParams['figure.figsize'] = 10, 8

#%% Parámetros del modelo
velocidad = 1.
Espacio=[30, 30]
Estados = ["Asintomaticos", "Enfermos", "Graves", "Recuperados", "Muertos"]

transmisor = {"Asintomaticos" : 14,
              "Enfermos"      : 21,
              "Graves"        : 25}

mortalidad = {"Asintomaticos" : 0.00,
              "Enfermos"      : 0.00,
              "Graves"        : 0.27}


tasas_contagios = {"Asintomaticos" : 0.30,
                   "Enfermos"      : 0.55,
                   "Graves"        : 0.15}

#%% La clase que contiene todo
class Poblacion():
    def __init__(self, N, **kwargs):
        
        self._poblacion = []
        
        tipos = {}
        
        for c in range(N):
            theta = rand()*2*pi # El ángulo de la velocidad con la que sale
            
            # Definimos a cada individuo
            p = {"Estado": "Sano",
                 "Posicion": [randint(Espacio[0]), randint(Espacio[1])],
                 "Velocidad": [velocidad*cos(theta), velocidad*sin(theta)],
                 "Dias" : 0}
            
            # Posicion : Posición que ocupa en el mapa
            # Velocidad: Es el vector que indica hacia donde se desplaza
            # Estado   : Indica su estado de salud
            # 
            
            
            self._poblacion.append(p)
            
        # Vamos convirtiendo
        for t in kwargs:
            for c in range(kwargs[t]):
                self._poblacion[randint(N)]["Estado"] = str(t)
    
    def nDias(self, dias):
        self._nDias = dias
        #self.DiaActual = 0
        return self
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.DiaActual += 1
        except AttributeError:
            self.DiaActual = 0
        
        
        if self.DiaActual >= self._nDias:
            raise StopIteration()
            
        self._mueve()
        
        
        return self
    
    def Recuento(self):
        salida = []
        N = len(self._poblacion)
        
        # Clasificamos la poblacione
        cuales = {e:[] for e in Estados}
        for p in self._poblacion:
            
            Estado = p["Estado"]

            if Estado in set(Estados):
                # Añadimos el individuo a la clase que le corresponde
                cuales[Estado].append(p)

            # Si está contagiado le contamos un dia más
            if Estado in set(Estados[0:3]):
                # Cambiamos de estado a los que ya han pasado la enfermedad
                if p["Dias"] > transmisor[Estado]:
                    # Comprobamos si ha muerto o se ha curado
                    azar = rand()
                    vel = array(p["Velocidad"])
                    
                    if azar < mortalidad[Estado]: # Ha muerto
                        p["Estado"] = Estados[4]
                        p["Velocidad"] = [0, 0]
                        
                    else: # Se ha curado y se vuelve inmune
                        p["Estado"] = Estados[3]
                        vel = vel/norm(vel)
                        p["Velocidad"] = list(vel)

                # Estaba entre los enfermos, le contamos un día más
                p["Dias"] += 1
            
            
        
        for e in Estados:
            salida.append(len(cuales[e]))
        
        return tuple(salida)
    
    def _mueve(self):
        '''Mueve a los individuos una iteración y comprueba contagios'''
        
        N = len(self._poblacion)
        
        # Primero los movemos todos
        for n, p in enumerate(self._poblacion):
            pos = array(p["Posicion"])
            vel = array(p["Velocidad"])
            
            posnueva = pos + vel * 1 #dt = 1
            
            # Comprobamos los contornos
            for c in range(2):
                if posnueva[c] <= 0:
                    posnueva[c] = 0.
                    vel[c] = -vel[c]
                elif posnueva[c] >= Espacio[c]:
                    posnueva[c] = Espacio[c]
                    vel[c] = -vel[c]

            # Actualizamos la posicion                    
            self._poblacion[n]["Posicion"] = list(posnueva)
            self._poblacion[n]["Velocidad"] = list(vel)

        # Detectamos coincidencias
        for c in range(N):
            p1 = self._poblacion[c]
            pos1 = round(p1["Posicion"])
            for d in range(c,N):
                p2 = self._poblacion[d]
                pos2 = round(p2["Posicion"])
                
                if all(pos1==pos2):
                    if _transmisor(p1):
                        _posible_contagio(p1,p2)
                    if _transmisor(p2):
                        _posible_contagio(p2, p1)


#%%
def _posible_contagio(transmisor, sano):
    '''Determina si hay un contagio entre dos individuos'''
    
    # Condiciones que no hacen posible el contagio
    if not(_transmisor(transmisor)): return
    if sano["Estado"] in set(Estados): return
    
    
    # Se dan las condiciones que hacen posible el contagio
    azar = rand()
    
    if azar <= 0.5: # Hay contagio
        azar2 = rand()
        
        if azar2 < tasas_contagios["Asintomaticos"]:
            sano["Estado"] = Estados[0]
        elif azar2 < tasas_contagios["Asintomaticos"] + tasas_contagios["Enfermos"]:
            sano["Estado"] = Estados[1]
        else:
            sano["Estado"] = Estados[2]
    
    sano["Dias"] = 0
    
#%%
def _transmisor(individuo):
    '''Determina si el individuo puede contagiar el patógeno'''
    
    Estado = individuo["Estado"]
    
    trans = set(Estados[0:3])
    if Estado in trans:
        return True
    else:
        return False


#%% Definimos la población
Pob = Poblacion(N=1000,
                Asintomaticos=3,
                Enfermos=1,
                Graves=0,
                Recuperados=0,
                Muertos=0)


#%% Iteramos para una serie de días
Asintomaticos = []
Enfermos = []
Graves = []
Recuperados = []
Muertos = []


for c in Pob.nDias(30*4):
    A, E, G, R, M = c.Recuento()
    
    print(c.DiaActual)
    
    # Lo dividimos por 10 para tenerlos en %
    Asintomaticos.append(A/10)
    Enfermos.append(E/10)
    Graves.append(G/10)
    Recuperados.append(R/10)
    Muertos.append(M/10)
    
    
#%% Salida
plt.rcParams['figure.figsize'] = 10, 8
plt.plot(Asintomaticos, label="Asintomáticos")
plt.plot(Enfermos, label="Enfermos")
plt.plot(Graves, label="Graves")
plt.plot(Recuperados, label="Recuperados")
plt.plot(Muertos, label="Muertos")
plt.xlabel("Tiempo (dias)")
plt.ylabel("% de la poblacion")

plt.legend(loc=0)


plt.show()