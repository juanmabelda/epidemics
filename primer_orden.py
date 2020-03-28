# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:54:55 2020

@author: jmbelda
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#%% solve the system dy/dt = f(y, t)
K = 3.
tau = 120

def f(y, t):
    
    Si = y[0]
    Ei = y[1]
     
    dSi  = -K*(5/tau)*Si
    dEi  = K*(5/tau)*Si - (5/tau)*Ei 
     
    return [dSi, dEi]
 
#%% initial conditions
S0 = 1
E0 = 0
y0 = [S0, E0]
t  = np.linspace(0, 140., 140) # 5 meses

#%% solve the DEs
soln = odeint(f, y0, t)
S = soln[:, 0]
E = soln[:, 1]

plt.plot(t, E)
plt.plot(t, S)