"Fabrication des graphiques pour l'analyse de donnée"
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

for n, heure in enumerate(hours): ### pour new_times l'indice 25555, pour hours l'indice 851
    if heure in ['2024-01-26 00:00']:
        print(n)


## Pour la stratification thermique, faire moyenne de chaque capteur par niveau (low, mid, top)
low_level = df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S29"] # permet de recuperer un intervalle de colonnes 
mid_level = df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S29"]
top_level = df.loc[:,"T[degC]-Top-S1":"T[degC]-Top-S29"]

## niveau low
new_low_level = []
for column_name, column_data in low_level.items():
    new_low_level.append(moyenne_par_heure(column_data))
# faire la moyenne par heure 
moy_low_level = np.nanmean(new_low_level, axis=0)

## niveau mid
new_mid_level = []
for column_name, column_data in mid_level.items():
    new_mid_level.append(moyenne_par_heure(column_data))
# faire la moyenne par heure 
moy_mid_level = np.nanmean(new_mid_level, axis=0)

## niveau top
new_top_level = []
for column_name, column_data in top_level.items():
    new_top_level.append(moyenne_par_heure(column_data))
# faire la moyenne par heure 
moy_top_level = np.nanmean(new_top_level, axis=0)

# ## fabriquer une figure pour strafication
figure = plt.figure(figsize=(8,5))
plt.plot(hours[851:], moy_top_level[851:], label='Hauteur 1.2m')
plt.plot(hours[851:], moy_mid_level[851:], label='Hauteur 0.8m')
plt.plot(hours[851:], moy_low_level[851:], label='Hauteur 0.4m')
plt.axvline(x=850, ymin=5, ymax=55, linewidth=43, linestyle="--", color='black',zorder=1)
# plt.xticks(np.arange(851, 1800, 180), rotation=20, fontsize=7)
plt.ylabel("Température [$^\circ$C]", fontsize=14)
plt.xlabel("Temps [H]", fontsize=14)
plt.legend()
plt.tight_layout()

#sauvegarde de la stratification
figure.savefig('StratificationThermiquePerHour26janv.png', dpi=1200)

## calculer la moyenne des capteurs par niveau (ordre croissant de niveau, low-mid-top)
# moy_level = [np.nanmean(low_level,axis=1),  np.nanmean(mid_level,axis=1),  np.nanmean(top_level,axis=1)]
## Temperature par plateau (ordre croissant de niveau, low-mid-top)
plateau_1 = [df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S5"], df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S5"], df.loc[:,"T[degC]-Top-S1":"T[degC]-Top-S5"]]
plateau_2 = [df.loc[:,"T[degC]-Low-S5":"T[degC]-Low-S9"], df.loc[:,"T[degC]-Mid-S5":"T[degC]-Mid-S9"], df.loc[:,"T[degC]-Top-S5":"T[degC]-Top-S9"]]
plateau_3 = [df.loc[:,"T[degC]-Low-S9":"T[degC]-Low-S13"], df.loc[:,"T[degC]-Mid-S9":"T[degC]-Mid-S13"], df.loc[:,"T[degC]-Top-S9":"T[degC]-Top-S13"]]
plateau_4 = [df.loc[:,"T[degC]-Low-S13":"T[degC]-Low-S19"], df.loc[:,"T[degC]-Mid-S13":"T[degC]-Mid-S19"], df.loc[:,"T[degC]-Top-S13":"T[degC]-Top-S19"]]
plateau_5 = [df.loc[:,"T[degC]-Low-S19":"T[degC]-Low-S23"], df.loc[:,"T[degC]-Mid-S19":"T[degC]-Mid-S23"], df.loc[:,"T[degC]-Top-S19":"T[degC]-Top-S23"]]
plateau_6 = [df.loc[:,"T[degC]-Low-S23":"T[degC]-Low-S29"], df.loc[:,"T[degC]-Mid-S23":"T[degC]-Mid-S29"], df.loc[:,"T[degC]-Top-S23":"T[degC]-Top-S29"]]

## gerer les plateaus avec l'approximation par heure
liste_plateau = [plateau_1, plateau_2, plateau_3, plateau_4, plateau_5, plateau_6]
liste_new_plateau = []
for plateau in liste_plateau:
    new_plateau = []

    for levels in plateau:
        new_level = []
        for column_name, column_data in levels.items():
            new_level.append(moyenne_par_heure(column_data))
        new_plateau.append(new_level)
    
    liste_new_plateau.append(new_plateau)

## Graphique de temperature par niveau pour le plateau 1 vs plateau 2
# liste_plateau = [plateau_1, plateau_2]

# faire plusieurs figure de plateau faire une boucle pour les 6 plateaux
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
            # axs[i].set_xticklabels(np.arange(0, 1800, 180), rotation=20, fontsize=7) ### modifier les labels fourni pour avoir les dates en heure


    # axs[i].axvline(x=20000, ymin=5, ymax=55, linewidth=43, linestyle="--", color='black',zorder=1)

## ameliorer positionnement du titre, avec top blabla..mise en forme latex
plt.suptitle('Évolution de la température moyenne sous chaque le plateau par niveau', fontsize=16)
f.supylabel("Température [$^\circ$C]", fontsize=14)
f.supxlabel("Temps [2 min]", fontsize=14)
f.legend()

# ##sauvegarder la figure:
# f.savefig('EvolutionTemperaturePlateauPerHour.png',dpi=1300)
print('cest fini')


###################################################################################### regle de controle
# regarder le capteur 1 et le capteur 29
# thermocouple_1 = [df['T[degC]-Low-S1'], df['T[degC]-Mid-S1'], df['T[degC]-Top-S1']]
# thermocouple_2 = [df['T[degC]-Low-S29'], df['T[degC]-Mid-S29'], df['T[degC]-Top-S29']]

# ## quantifier par heure
# moy_thermocouple_1 = []
# for level in thermocouple_1:
#     for column_name, column_data in level.items():
#         moy_thermocouple_1.append(moyenne_par_heure(column_data))
    

# print(len(moy_thermocouple_1))
# print(len(moy_thermocouple_1[0]))


