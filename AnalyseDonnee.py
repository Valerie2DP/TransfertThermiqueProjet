import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_csv("measurements.csv", delimiter=";")

## Pour la stratification thermique
# low_level = df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S29"] # permet de recuperer un intervalle de colonnes 
# mid_level = df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S29"]
# top_level = df.loc[:,"T[degC]-Top-S1":"T[degC]-Low-S29"]

## calculer la moyenne des capteurs par niveau (ordre croissant de niveau, low-mid-top)
# moy_level = [np.nanmean(low_level,axis=1),  np.nanmean(mid_level,axis=1),  np.nanmean(top_level,axis=1)]

## Temperature par plateau (ordre croissant de niveau, low-mid-top)
plateau_1 = [df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S5"], df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S5"], df.loc[:,"T[degC]-Top-S1":"T[degC]-Top-S5"]]
plateau_2 = [df.loc[:,"T[degC]-Low-S5":"T[degC]-Low-S9"], df.loc[:,"T[degC]-Mid-S5":"T[degC]-Mid-S9"], df.loc[:,"T[degC]-Top-S5":"T[degC]-Top-S9"]]
plateau_3 = [df.loc[:,"T[degC]-Low-S9":"T[degC]-Low-S13"], df.loc[:,"T[degC]-Mid-S9":"T[degC]-Mid-S13"], df.loc[:,"T[degC]-Top-S9":"T[degC]-Top-S13"]]
plateau_4 = [df.loc[:,"T[degC]-Low-S13":"T[degC]-Low-S19"], df.loc[:,"T[degC]-Mid-S13":"T[degC]-Mid-S19"], df.loc[:,"T[degC]-Top-S13":"T[degC]-Top-S19"]]
plateau_5 = [df.loc[:,"T[degC]-Low-S19":"T[degC]-Low-S23"], df.loc[:,"T[degC]-Mid-S19":"T[degC]-Mid-S23"], df.loc[:,"T[degC]-Top-S19":"T[degC]-Top-S23"]]
plateau_6 = [df.loc[:,"T[degC]-Low-S23":"T[degC]-Low-S29"], df.loc[:,"T[degC]-Mid-S23":"T[degC]-Mid-S29"], df.loc[:,"T[degC]-Top-S23":"T[degC]-Top-S29"]]

## Graphique de temperature par niveau pour le plateau 1 vs plateau 2
liste_niveau = ['Low','Mid','Top']
liste_plateau = [plateau_1, plateau_2, plateau_3, plateau_4, plateau_5, plateau_6]
# liste_plateau = [plateau_1, plateau_2]

# faire plusieurs figure de plateau faire une boucle pour les 6 plateaux
f, axs = plt.subplots(6, 1,figsize=(10,8), sharex=True)

#un graphique par plateau
for i, plateau in enumerate(liste_plateau):
    if i == 0:
        ## plot courbe de chaque niveau par plateau
        for n, level in enumerate(plateau):
            # calcul de la moyenne des capteurs
            moy_plateau = np.nanmean(level, axis=1)
            axs[i].plot(np.arange(len(moy_plateau)), moy_plateau, label=liste_niveau[n], zorder=0)

    else:
        ## plot courbe de chaque niveau par plateau
        for n, level in enumerate(plateau):
            # calcul de la moyenne des capteurs
            moy_plateau = np.nanmean(level, axis=1)
            axs[i].plot(np.arange(len(moy_plateau)), moy_plateau, zorder=0)

    axs[i].axvline(x=20000, ymin=5, ymax=55, linewidth=43, linestyle="--", color='black',zorder=1)

## ameliorer positionnement du titre, avec top blabla
plt.suptitle('Évolution de la température moyenne sous chaque le plateau par niveau', fontsize=16)
f.supylabel("Température [$^\circ$C]", fontsize=14)
f.supxlabel("Temps [2 min]", fontsize=14)
f.legend()

##sauvegarder la figure:
f.savefig('EvolutionTemperaturePlateau.png',dpi=200)
print('cest fini')


# # lire les capteurs en dessous du plateau 1.. niveau low
# # eventuellement faire une boucle pour simplifier
# df1 = pd.read_csv("measurements.csv", delimiter=";", usecols=['Time','T[degC]-Low-S1']) ## skiprows=25557 ne marche pas car on ne peut specifier le nom de colonnes
# df2 = pd.read_csv("measurements.csv", delimiter=";", usecols=['Time','T[degC]-Low-S2']) ## skiprows=25557 ne marche pas car on ne peut specifier le nom de colonnes
# df3 = pd.read_csv("measurements.csv", delimiter=";", usecols=['Time','T[degC]-Low-S3']) ## skiprows=25557 ne marche pas car on ne peut specifier le nom de colonnes
# df4 = pd.read_csv("measurements.csv", delimiter=";", usecols=['Time','T[degC]-Low-S4']) ## skiprows=25557 ne marche pas car on ne peut specifier le nom de colonnes
# df5 = pd.read_csv("measurements.csv", delimiter=";", usecols=['Time','T[degC]-Low-S5']) ## skiprows=25557 ne marche pas car on ne peut specifier le nom de colonnes

# # graphique tres primitif de levolution en fonction du temps
# # ignorer les donnees avant le 26 janvier, index 25557 dans le csv a la date 2024-01-26
# start = 2557
# plateau1_low = [(df1[start:]),(df2[start:]),(df3[start:]),(df4[start:]),(df5[start:])]


# # set une courbe de temperature pour un capteur
# # ax = plateau1_low[0].plot()

# # plot les autres capteurs sur la meme figure
# for n, data in enumerate(plateau1_low):
#     if n ==0:
#         ax = data.plot()
#     else:
#         data.plot(ax=ax)

# plt.show()
