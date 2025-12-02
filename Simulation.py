import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

#Paramètres physiques
m =
cp =
C1 = m*cp
R1 = #Résistance tehrmique de la dalle
R2 = #Résistance thermique de l'isolant
#Maillage
H = 2.2 #mètres
m = 3
dy = H/m

dt = 1
nt = 1800

T = np.zeros((nt+1, m+1)) #matrice y t

#Condition limite
for t in range (0,1800):
    T[t, m] = #Prendre les données de Text à chaque heure dans CSV

#T entre dalle et isolant
for t in range (0,1800):
    for j in range (1, m-1, -1):
        T[t, j] = T[t-1, j] * dt/C1 + T[t]  #Prendre les données de Text à chaque heure dans CSV