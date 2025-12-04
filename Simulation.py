import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

#Paramètres physiques
Long = 26.1 #m
larg = 3.7 #m
Haut = 1.7 #m
k_beton =
h_air =
k_asph = 
k_acier = 
q_heater1 = 10000 #W
q_heater2 = 7500 #W
##Débit d'air entre les zones
a12 = 0.2381
a21	= 0.4438
a23	= 0.3268
a32	= 0.7042
a34	= 0.2646
a43	= 0.5915
a45	= 0.1988
a54	= 0.2915
a56	= 0.4694
a65	= 0.4070

#Initalisation
dt = 1
nt = 1800

T3 = np.zeros((nt, m)) #matrice y t

#Système matriciel
T = np.zeros((9,1)) 
M = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
B = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
#Résolution
for t in range (0,1800):    
