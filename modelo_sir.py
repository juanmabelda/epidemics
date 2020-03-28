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
plt.rcParams['figure.figsize'] = 10, 8

#%%
beta = 1e-7 # Coeficiente de transmisión
gamma = 1/14  # Tasa de recuperación 

#%% solve the system dy/dt = f(y, t)
def sir(y, t):
     Si  = y[0] # Sanos
     Ii  = y[1] # Contagiados  
     Ri  = y[2] # Recuperados
     
     # La tasa de sanos
     dSi  = -beta*Si*Ii
     dIi  =  beta*Si*Ii - gamma*Ii
     dRi  =  gamma*Ii
     
     return [dSi, dIi, dRi]

#%% initial conditions
S0 = 4520000.   # Población inicial
I0 = 15       # initial death population
R0 = 0
y0 = [S0, I0, R0]     # initial condition vector
t  = np.linspace(0, 140., 140) # 5 meses

#%% solve the DEs
soln = odeint(sir, y0, t)
S = soln[:, 0]
I = soln[:, 1]
R = soln[:, 2]

#%% plot results
plt.figure()
plt.plot(t, S, label='Sanos')
plt.plot(t, I, label='Infectados')
plt.plot(t, R, label='Recuperados')
plt.xlabel('Días desde el brote')
plt.ylabel('Población')
plt.title('Infeccion COVID19')
plt.legend(loc=0)

#%%
plt.show()