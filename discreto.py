# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:34:36 2020

@author: jmbelda
"""

import numpy as np
import matplotlib.pyplot as plt


#%%
plt.ion()
plt.rcParams['figure.figsize'] = 15, 8

#%%
P = [4.5e6]
E = [15]
C = [2*E[0]]
R = [0]
M = [0]


#%% Dias de recuperacion y tasas de recuperación

# =============================================================================
# Escenario bastante malo
# dC = 13
# dE = 13
# 
# tC = 1.
# tE = 0.98
# 
# Tasa de contagio
# rc = 4/15
# =============================================================================


# =============================================================================
# Escenario más realista
# dC = 13
# dE = 13
#  
# tC = 1.
# tE = 0.98
#  
# Tasa de contagio
# rc = 3.6/15
# =============================================================================

# =============================================================================
# Todos contagiados
# dC = 13
# dE = 13
# 
# tC = 1.
# tE = 0.98
# 
# # Tasa de contagio
# rc = 5/15
# =============================================================================


dC = 21
dE = 21
#  
tC = 1.
tE = 0.98
#  
# Tasa de contagio
rc = 2.5/15



#%% Tasa de contagiados
for c in range(1, 90):
    TEC = np.floor(rc*(E[c-1]+C[c-1])) # Cada contagiado, contagia a rc mas
        
    # Los sacamos de los sanos, que son los únicos que pueden
    if (TEC > P[c-1]):
        TEC = P[c-1]
    
    P.append(P[c-1]-TEC) # La nueva poblacion
    
    # Sacamos los nuevos enfermos y los nuevos contaciados
    nE = np.floor(TEC/3)
    nC = TEC - nE
    
    
    # Vamos con los contagiados recuperados
    if c > dC:
        nRC = np.floor(C[c-dC-1]*tC)
    else:
        nRC = 0
        
    if c > dE:
        nRE = np.floor(E[c-dE-1]*tE)
        nM  = E[c-dE-1] - nRE # Número de muertos
    else:
        nRE = 0
        nM = 0
    
    Ei = E[c-1]+nE-nRE-nM
    if Ei <0 :
        nRnM = E[c-1]+nE
        
        nRE = np.floor(nRnM*tE)
        nM  = nRnM - nRE
        Ei = E[c-1]+nE-nRE-nM
    
    Ci = C[c-1]+nC-nRC
    if Ci<0 :
        nRC = C[c-1]+nC
        Ci = C[c-1]+nC-nRC
    
    R.append(R[c-1] + nRC + nRE)            

    #if nM < 0: nM=0
    
    M.append(M[c-1]+nM)
    E.append(Ei)
    C.append(Ci)
        
        #print(M[c]+P[c]+R[c]+E[c]+C[c])

        
#%% Los gráficos
ax = plt.subplot(3,1,1)
plt.plot(P, label='Sanos')
plt.plot(R, label='Recuperados')
plt.legend(loc=0)
plt.title('Infeccion COVID19')

plt.subplot(3,1,2, sharex=ax)
plt.plot(E, label='Enfermos')
plt.plot(C, label='Asintomáticos')
plt.legend(loc=0)

plt.subplot(3,1,3,sharex=ax)
plt.plot(M, label='Fallecidos')
plt.legend(loc=0)
plt.xlabel('Tiempo (días)')

#%% La tasa de muertos
TasaMuertos = [100*M[c]/max(E[0:c]) for c in range(1,90)]
    
plt.figure();
plt.plot(TasaMuertos)
       