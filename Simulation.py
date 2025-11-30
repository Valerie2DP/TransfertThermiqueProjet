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

T = np.zeros(m+1, n+1)

temps = 1800 #heures

#Conditions limites
for i in range (0, n):
 T[i, :] = 