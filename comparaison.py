from Simulation import T2
from AnalyseDonnee import liste_moy_per_plateau
import matplotlib.pyplot as plt
import numpy as np

## valeur de la simulation de la moyennes de capteurs de toutes les hauteurs (0.4, 0.8, 1.2) par 2 plateaux, en heures
Simu_P1P2 = T2[:, 0]
Simu_P3P4 = T2[:, 1]
Simu_P5P6 = T2[:, 2]

## valeur des mesures de la moyennes des capteurs de toutes les hauteurs (0.4, 0.8, 1.2) par 2 plateaux, en heures
Temp_P1P2 =  [(P1 + P2) / 2 for P1, P2 in zip(liste_moy_per_plateau[0], liste_moy_per_plateau[1])].pop(0)
Temp_P3P4 =  [(P3 + P4) / 2 for P3, P4 in zip(liste_moy_per_plateau[2], liste_moy_per_plateau[3])].pop(0)
Temp_P5P6 =  [(P5 + P6) / 2 for P5, P6 in zip(liste_moy_per_plateau[4], liste_moy_per_plateau[5])].pop(0)

## faire figure de comparaison
fig = plt.figure()
axe_x = np.arange(0,len(Simu_P1P2))
plt.plot(axe_x, Simu_P1P2, color='red', label='Simulation P1 et P2')
plt.plot(axe_x, Temp_P1P2, color='blue', label='Mesures P1 et P2')
plt.xlabel('Temps [h]')
plt.legend()
plt.show()