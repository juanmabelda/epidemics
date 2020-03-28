# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 08:10:56 2020

@author: jmbelda
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#............................................................................
# Cosas que sabemos

'''
La tasa de enfermos se duplica cada 3 días (sin confinamiento)
La tasa de contagiados sanos o leves es el doble que la de enfermos
Cada persona contagiada contagia a otros 3 (sin confinamiento)

Un contagiado leve tarda unos dos días en recuperarse
Un contagiado enfermo tarda unos 15 días en recuperarse

El 2% de los contagiados enfermos se muere
 
'''

#%%
plt.ion()
plt.rcParams['figure.figsize'] = 10, 8

#%%
a  = 3e-7    # Contagiados por día
b1 = 0.002   # Recuperados por día (asintomáticos)
b2 = 0.001   # Recuperados por día (enfermos)
c  = 0.01    # Enfermos por día contagiados
d  = 0.001   # Muertos por día (Enfermos)

#%% solve the system dy/dt = f(y, t)
def f(y, t):
     Si  = y[0] # Sanos
     Ci  = y[1] # Contagiados  
     Ei  = y[2] # Enfermos
     Ri  = y[3]
     Mi  = y[4] # Muertos
     
     # La tasa de sanos
     dSi  = -3*a*Si*Ei
     dEi  =    a*Si*Ei - (0.98*5/10)*Ei - (0.02*5/10)*Ei
     dCi  =  2*a*Si*Ei - (5/2)*Ci
     dRi  =  Ri + (5/2)*Ci + (0.98*5/10)*Ei
     dMi  =  Mi + (0.02*5/10)*Ei
     
     return [dSi, dCi, dEi, dRi, dMi]

#%% initial conditions
S0 = 4520000.   # Población inicial
C0 = 0        # initial zombie population
E0 = 15       # initial death population
R0 = 0
M0 = 0
y0 = [S0, C0, E0, R0, M0]     # initial condition vector
t  = np.linspace(0, 140., 140) # 5 meses

#%% solve the DEs
soln = odeint(f, y0, t)
S = soln[:, 0]
C = soln[:, 1]
E = soln[:, 2]
R = soln[:, 3]
M = soln[:, 4]

#%% plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, S, label='Sanos')
plt.plot(t, C, label='Contagiados')
plt.xlabel('Días desde el brote')
plt.ylabel('Población')
plt.title('Infeccion COVID19')
plt.legend(loc=0)
plt.subplot(2,1,2)
plt.plot(t, E, label='Enfermos')
plt.plot(t, M, label='Muertos')
plt.xlabel('Días desde el brote')
plt.ylabel('Población')
#plt.title('Infeccion COVID19')
plt.legend(loc=0)
