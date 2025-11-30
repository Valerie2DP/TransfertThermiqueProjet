import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

#Paramètres physiques

#Maillage
L = 26.1 #mètres
n = 4
dx = L/n

H = 2.2 #mètres
m = 3
dy = H/m

dt = 1
nt = 1800

T = np.zeros((m+1, n+1)) #matrice x y
T_hist = np.zeros((nt+1, m+1)) #matrice xy t

#Conditions limites
for t in range (0,1800):
    for i in range (0, n):
        T[i, :] = 