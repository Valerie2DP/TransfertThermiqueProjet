import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv("measurements.csv", delimiter=";")

## recupere les dates heure et minutes de l'acquisition de donnée du .csv
time = df["Time"]
new_times = []
for t in time:
    dt_values = datetime.strptime(t, "%Y-%m-%d %H:%M")
    new_times.append(dt_values.strftime("%Y-%m-%d %H:%M"))

## permet de garder les heures piles
def heures_correspondantes(timestamps):
    """
    Prend une liste de timestamps au format '%Y-%m-%d %H:%M'
    et retourne une liste contenant un timestamp par heure,
    pour correspondre aux moyennes horaires.
    """

    heures = []
    derniere_heure = None

    for ts in timestamps:
        # Convertit le string en datetime
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        
        # Si on change d'heure → on garde ce timestamp
        if dt.hour != derniere_heure:
            heures.append(ts)
            derniere_heure = dt.hour

    return heures[1:-1]
hours = heures_correspondantes(new_times)

def moyenne_par_heure(temperatures):
    """Retourne une liste de moyennes horaires à partir 
    de données prises aux 2 minutes.
    
    Paramètres:
        temperatures (list of float): données brutes
        
    Retour:
        list of float: moyennes par heure
    """
    moyennes = []
    #print(hours)

    pas = 30  # 30 valeurs = 1 heure

    for y in range(25, len(temperatures), pas):
        bloc = temperatures[y:y+pas]
        if len(bloc) == pas:  # on ignore les blocs incomplets à la fin
            moyennes.append(sum(bloc) / pas)

    return moyennes


## Pour la stratification thermique, faire moyenne de chaque capteur par niveau 
low_level = df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S29"] # permet de recuperer un intervalle de colonnes 
mid_level = df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S29"]
top_level = df.loc[:,"T[degC]-Top-S1":"T[degC]-Low-S29"]

new_low_level = []
for temperature in low_level:
    print(len(temperature))
    new_low_level.append(moyenne_par_heure(temperature))

print(np.shape(low_level))
print(type(low_level))

# new_mid_level = []
# for temperature in mid_level:
#     new_mid_level.append(moyenne_par_heure(temperature))
    
# new_top_level = []
# for temperature in top_level:
#     new_top_level.append(moyenne_par_heure(temperature))

print(len(low_level))
# print(len(new_low_level))

# ## fabriquer une figure pour strafication
# figure = plt.figure()
# plt.plot(hours, np.nanmean(new_low_level), axis=1)
# plt.plot(hours, np.nanmean(new_mid_level), axis=1)
# plt.plot(hours, np.nanmean(new_top_level), axis=1)
# plt.show()


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
f.savefig('EvolutionTemperature2Plateau.png',dpi=200)
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
