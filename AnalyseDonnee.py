"Fabrication des graphiques pour l'analyse de donnée"
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv("/Users/smg/GitHub/transfert thermique/TransfertThermiqueProjet/measurements.csv", delimiter=";")

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




# ###################################################################################### regle de controle
# # regarder le capteur 1 et le capteur 29 et temperature exterieur
# # temperature du milieu pour les capteurs, regarder la températures extérieur

thermocouple_1 =  df['T[degC]-Mid-S1']
thermocouple_2 =  df['T[degC]-Mid-S29']
Texterieur = df['Outdoor temperature [deg. C]']

# ## fabrication de figure
# fig, axes = plt.subplots(3,1,figsize=(8,8),sharex=True)
# axes_x = np.arange(len(Texterieur[25555:]))

# ## fabriquer les intersections... entre 3 et temperature ext
# axes[0].plot(axes_x, Texterieur[25555:], label='Température extérieur')
# axes[0].plot(axes_x, [3]*len(axes_x))
# axes[1].plot(axes_x, thermocouple_1[25555:], label='Thermocouple S1')
# axes[2].plot(axes_x, thermocouple_2[25555:], label='Thermocouple S29')
# # axes[2].set_xticks(new_xtick, new_hourslabel, rotation=20, fontsize=9)
# fig.legend()

# plt.show()


# ## Pour la stratification thermique, faire moyenne de chaque capteur par niveau (low, mid, top)
# low_level = df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S29"] # permet de recuperer un intervalle de colonnes 
# mid_level = df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S29"]
# top_level = df.loc[:,"T[degC]-Top-S1":"T[degC]-Top-S29"]

# ## niveau low
# new_low_level = []
# for column_name, column_data in low_level.items():
#     new_low_level.append(moyenne_par_heure(column_data))
# # faire la moyenne par heure 
# moy_low_level = np.nanmean(new_low_level, axis=0)

# ## niveau mid
# new_mid_level = []
# for column_name, column_data in mid_level.items():
#     new_mid_level.append(moyenne_par_heure(column_data))
# # faire la moyenne par heure 
# moy_mid_level = np.nanmean(new_mid_level, axis=0)

# ## niveau top
# new_top_level = []
# for column_name, column_data in top_level.items():
#     new_top_level.append(moyenne_par_heure(column_data))
# # faire la moyenne par heure 
# moy_top_level = np.nanmean(new_top_level, axis=0)

# # ## fabriquer une figure pour strafication, donnee a partir du 26 janvier... donc avec les heure pile a partir du 851 indices
# figure = plt.figure(figsize=(9,5))

# ## formating necessaire pour avoir des heures apres le 26 janvier
# new_xtick = list(np.arange(0,949, 94))
# new_hourslabel = [hours[851:][n] for n in new_xtick]

# plt.plot(hours[851:], moy_top_level[851:], label='Hauteur 1.2m',color='blue')
# plt.plot(hours[851:], moy_mid_level[851:], label='Hauteur 0.8m',color='darkorange')
# plt.plot(hours[851:], moy_low_level[851:], label='Hauteur 0.4m',color='green')
# plt.xticks(new_xtick, new_hourslabel, rotation=20, fontsize=9)
# plt.ylabel("Température [$^\circ$C]", fontsize=14)
# plt.xlabel("Temps [h]", fontsize=14)
# plt.legend()
# plt.tight_layout()

# #sauvegarde de la stratification
# figure.savefig('StratificationThermiquePerHour26janv.png', dpi=1200)

# ## calculer la moyenne des capteurs par niveau (ordre croissant de niveau, top-mid-low)
# # moy_level = [np.nanmean(low_level,axis=1),  np.nanmean(mid_level,axis=1),  np.nanmean(top_level,axis=1)]
# ## Temperature par plateau (ordre croissant de niveau, low-mid-top)
# plateau_1 = [df.loc[:,"T[degC]-Top-S1":"T[degC]-Top-S5"], df.loc[:,"T[degC]-Mid-S1":"T[degC]-Mid-S5"], df.loc[:,"T[degC]-Low-S1":"T[degC]-Low-S5"]]
# plateau_2 = [df.loc[:,"T[degC]-Top-S5":"T[degC]-Top-S9"], df.loc[:,"T[degC]-Mid-S5":"T[degC]-Mid-S9"], df.loc[:,"T[degC]-Low-S5":"T[degC]-Low-S9"]]
# plateau_3 = [df.loc[:,"T[degC]-Top-S9":"T[degC]-Top-S13"], df.loc[:,"T[degC]-Mid-S9":"T[degC]-Mid-S13"], df.loc[:,"T[degC]-Low-S9":"T[degC]-Low-S13"]]
# plateau_4 = [df.loc[:,"T[degC]-Top-S13":"T[degC]-Top-S19"], df.loc[:,"T[degC]-Mid-S13":"T[degC]-Mid-S19"], df.loc[:,"T[degC]-Low-S13":"T[degC]-Low-S19"]]
# plateau_5 = [df.loc[:,"T[degC]-Top-S19":"T[degC]-Top-S23"], df.loc[:,"T[degC]-Mid-S19":"T[degC]-Mid-S23"], df.loc[:,"T[degC]-Low-S19":"T[degC]-Low-S23"]]
# plateau_6 = [df.loc[:,"T[degC]-Top-S23":"T[degC]-Top-S29"], df.loc[:,"T[degC]-Mid-S23":"T[degC]-Mid-S29"], df.loc[:,"T[degC]-Low-S23":"T[degC]-Low-S29"]]

# ## gerer les plateaus avec l'approximation par heure
# liste_plateau = [plateau_1, plateau_2, plateau_3, plateau_4, plateau_5, plateau_6]
# liste_moy_per_level_new_plateau = []
# liste_new_plateau = []

# for plateau in liste_plateau:
#     new_plateau = []
#     for levels in plateau:
#         new_level = []
#         for column_name, column_data in levels.items():
#             new_level.append(moyenne_par_heure(column_data))
#         new_plateau.append(new_level)
    
#     # ajouter les moyennes par niveau de chaque plateau par heure
#     liste_new_plateau.append(new_plateau)
#     # ajouter la moyenne des trois niveau par plateau par heure
#     liste_moy_per_level_new_plateau.append(np.nanmean(new_plateau, axis=1))

# ## moyenne de chaque niveau par plateau
# liste_moy_per_plateau = []
# for plateau in liste_moy_per_level_new_plateau:
#     liste_moy_per_plateau.append(np.nanmean(plateau, axis=0))

# # Faire plusieurs figure de plateau faire une boucle pour les 6 plateaux
# f, axs = plt.subplots(6, 1,figsize=(10,8), sharex=True)
# liste_nom_plateau = ['P1','P2','P3','P4','P5','P6']
# liste_couleur = ['blue', 'green', 'purple', 'darkorange', 'cornflowerblue', 'firebrick']

# for i, plateau in enumerate(liste_moy_per_plateau):
#     axs[i].plot(hours[851:], plateau[851:], label=liste_nom_plateau[i], color=liste_couleur[i],zorder=0)
#     axs[i].set_xticks(new_xtick, new_hourslabel, rotation=20, fontsize=9)
# f.supylabel("Température [$^\circ$C]", fontsize=14)
# f.supxlabel("Temps [h]", fontsize=14)
# f.legend(bbox_to_anchor=(0.98,0.98))

# ##sauvegarder la figure:
# f.savefig('EvolutionTemperatureMoyPlateauPerHour.png', dpi=1300) ### gros probleme a suivre

## recuperer les dates
temperature_apres_26 = Texterieur[25557:]
date_importante = []
for i, element in enumerate(temperature_apres_26):
    if 3 <= element <= 3.05:
        date_importante.append(i)

print(date_importante)


# faire figure recapitulative de temperature exterieur et des capteurs S1 et S29
figure_regle, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(10,8), sharex=True)
axe_x = np.arange(0,len(Texterieur))[25557:]

## plot la température extérieur
ax1.plot(axe_x, temperature_apres_26, label='Température extérieur', color='blue')
ax1.plot(axe_x, [3]*len(axe_x),color='orchid', label='seuil de 3 degree')
ax2.plot(axe_x, thermocouple_2[25557:], label='Thermocouple 2', color='darkorange')
ax3.plot(axe_x, thermocouple_1[25557:], label='Thermocouple 1', color='green')
figure_regle.supylabel("Température [$^\circ$C]", fontsize=14)
figure_regle.legend()



plt.show()

