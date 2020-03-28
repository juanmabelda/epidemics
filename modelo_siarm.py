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
#plt.ion()
plt.rcParams['figure.figsize'] = 10, 8

#%%
beta1 = 1e-7 # Coeficiente de transmisión
beta2 = 1.01*beta1
gamma21 = 1/14
gamma11 = 0.98/14  # Tasa de recuperación
gamma12 = 0.02/14  # Tasa de fallecimientos 

#%% solve the system dy/dt = f(y, t)
def sir(y, t):
     Si  = y[0] # Sanos
     Ii  = y[1] # Contagiados 
     Ai  = y[2] # Asintomáticos
     Ri  = y[3] # Recuperados
     Mi  = y[4] # Fallecidos
     
     # La tasa de sanos
     dSi  = -beta1*Si*Ii - beta2*Si*Ai
     dIi  =  beta1*Si*Ii - gamma11*Ii  - gamma12*Ii
     dAi  =  beta2*Si*Ai - gamma21*Ai
     dRi  =  gamma11*Ii  + gamma21*Ai
     dMi  =  gamma12*Ii
     
     return [dSi, dIi, dAi, dRi, dMi]

#%% initial conditions
S0 = 4520000.   # Población inicial
I0 = 15       # initial death population
R0 = 0
A0 = 2*I0
M0 = 0
y0 = [S0, I0, A0, R0, M0]     # initial condition vector
t  = np.linspace(0, 140., 140) # 5 meses

#%% solve the DEs
soln = odeint(sir, y0, t)
S = soln[:, 0]
I = soln[:, 1]
A = soln[:, 2]
R = soln[:, 3]
M = soln[: ,4]

#%% plot results
plt.figure()
plt.plot(t, S, label='Sanos')
plt.plot(t, I, label='Infectados')
plt.plot(t, A, label='Asintomáticos')
plt.plot(t, R, label='Recuperados')
plt.plot(t, M, label='Muertos')
plt.xlabel('Días desde el brote')
plt.ylabel('Población')
plt.title('Infeccion COVID19')
plt.legend(loc=0)

plt.show()
