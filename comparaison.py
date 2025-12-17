from Simulation import T2
from AnalyseDonnee import liste_moy_per_plateau
import matplotlib.pyplot as plt
import numpy as np

## valeur de la simulation de la moyennes de capteurs de toutes les hauteurs (0.4, 0.8, 1.2) par 2 plateaux, en heures
Simu_P1P2 = T2[:, 2]
Simu_P3P4 = T2[:, 1]
Simu_P5P6 = T2[:, 0]

## valeur des mesures de la moyennes des capteurs de toutes les hauteurs (0.4, 0.8, 1.2) par 2 plateaux, en heures
Temp_P1P2 =  [(P1 + P2) / 2 for P1, P2 in zip(liste_moy_per_plateau[0], liste_moy_per_plateau[1])]
Temp_P3P4 =  [(P3 + P4) / 2 for P3, P4 in zip(liste_moy_per_plateau[2], liste_moy_per_plateau[3])]
Temp_P5P6 =  [(P5 + P6) / 2 for P5, P6 in zip(liste_moy_per_plateau[4], liste_moy_per_plateau[5])]

## Figure de comparaison de la simulation et des mesures
fig, (ax1, ax2, ax3)  = plt.subplots(ncols=1, nrows=3, sharex=True, figsize=(8,6))

## comparaison des valeurs de P1 et P2
ax1.plot(np.arange(0,len(Simu_P1P2)), Simu_P1P2, color='red', label='Simulation P1 et P2')
ax1.plot(np.arange(0,len(Temp_P1P2)), Temp_P1P2, color='blue', label='Mesures P1 et P2')
ax1.legend(loc='lower left')

## comparaison des valeurs de P3 et P4
ax2.plot(np.arange(0,len(Simu_P3P4)), Simu_P3P4, color='red', label='Simulation P3 et P4')
ax2.plot(np.arange(0,len(Temp_P3P4)), Temp_P3P4, color='blue', label='Mesures P3 et P4')
ax2.legend(loc='upper left')

## comparaison des valeurs de P5 et P6
ax3.plot(np.arange(0,len(Simu_P5P6)), Simu_P5P6, color='red', label='Simulation P5 et P6')
ax3.plot(np.arange(0,len(Temp_P5P6)), Temp_P5P6, color='blue', label='Mesures P5 et P6')
ax3.legend(loc='upper left')

# fig.suptitle('Comparaison température moyenne de la simulation\n et des mesures par regroupement de plateaux')
fig.supylabel('Température [$^{\circ}$C]')
fig.supxlabel('Temps [h]')

fig.savefig('Comparaison-Simulation-Mesures-Regroupement-2Plateaux-v15-regle08-new.png',dpi=1300)