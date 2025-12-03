import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create sample DataFrame
data = pd.DataFrame({'Unit': [5, 15, 20, 25, 30, 40, 45, 50]})

# Bin the Age column into 3 equal-sized bins
data['UnitGroup'] = pd.cut(data['Unit'], bins=3)

# Print the DataFrame
date = '2023-12-21 12:20'
print(len(date))


# demonstration de montrer la date du 26 janvier 2024
x = [n for n in range(1,50)]
y = 0.2*np.array(x)

plt.plot(x,y)
plt.axvline(x=20, ymin=0, ymax=10, linewidth=70, linestyle="--", color='black')
plt.show()


########################################################################## ancien graphique pour levolution de la temperature par plateau avec les 3 niveaux
f, axs = plt.subplots(6, 1,figsize=(10,8), sharex=True)
liste_niveau = ['Low','Mid','Top'] ## eventuellementchang
#un graphique par plateau... # incorporer la quantification par heure dans le temps
for i, plateau in enumerate(liste_new_plateau):
    if i == 0:
        ## plot courbe de chaque niveau par plateau
        for n, level in enumerate(plateau):
            # calcul de la moyenne des capteurs
            moy_plateau = np.nanmean(level, axis=0) ## axis = 0 pour liste de plateau en 2min
            axs[i].plot(np.arange(len(moy_plateau)), moy_plateau, label=liste_niveau[n], zorder=0)

    else:
        ## plot courbe de chaque niveau par plateau
        for n, level in enumerate(plateau):
            # calcul de la moyenne des capteurs
            moy_plateau = np.nanmean(level, axis=0) ## axis = 0 pour liste de plateau en 2min
            axs[i].plot(np.arange(len(moy_plateau)), moy_plateau, zorder=0)
            



## ameliorer positionnement du titre, avec top blabla..mise en forme latex
plt.suptitle('Évolution de la température moyenne sous chaque le plateau par niveau', fontsize=16)
f.supylabel("Température [$^\circ$C]", fontsize=14)
f.supxlabel("Temps [2 min]", fontsize=14)
f.legend()
