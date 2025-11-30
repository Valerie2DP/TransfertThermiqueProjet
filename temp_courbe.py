import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import norm


file_path = "/Users/smg/GitHub/transfert thermique/TransfertThermiqueProjet/measurements.csv"
df = pd.read_csv(file_path, delimiter=";")

time = df["Time"]
new_times = []
for t in time:
    dt_values = datetime.strptime(t, "%Y-%m-%d %H:%M")
    new_times.append(dt_values.strftime("%Y-%m-%d %H:%M"))

df_out_temp = df["Outdoor temperature [deg. C]"]
df_out_hum = df["Outdoor relative humidity [%]"]
#print(new_times)

# Low
df1 = df["T[degC]-Low-S1"]
df2 = df["T[degC]-Low-S2"]
df3 = df["T[degC]-Low-S3"]
df4 = df["T[degC]-Low-S4"]
df5 = df["T[degC]-Low-S5"]
df6 = df["T[degC]-Low-S6"]
df7 = df["T[degC]-Low-S7"]
df8 = df["T[degC]-Low-S8"]
df9 = df["T[degC]-Low-S9"]
df10 = df["T[degC]-Low-S10"]
df11 = df["T[degC]-Low-S11"]
df12 = df["T[degC]-Low-S12"]
df13 = df["T[degC]-Low-S13"]
df14 = df["T[degC]-Low-S14"]
df15 = df["T[degC]-Low-S15"]
df16 = df["T[degC]-Low-S16"]
df17 = df["T[degC]-Low-S17"]
df18 = df["T[degC]-Low-S18"]
df19 = df["T[degC]-Low-S19"]
df20 = df["T[degC]-Low-S20"]
df21 = df["T[degC]-Low-S21"]
df22 = df["T[degC]-Low-S22"]
df23 = df["T[degC]-Low-S23"]
df24 = df["T[degC]-Low-S24"]
df25 = df["T[degC]-Low-S25"]
df26 = df["T[degC]-Low-S26"]
df27 = df["T[degC]-Low-S27"]
df28 = df["T[degC]-Low-S28"]
df29 = df["T[degC]-Low-S29"]


# Middle
df1m = df["T[degC]-Mid-S1"]
df2m = df["T[degC]-Mid-S2"]
df3m = df["T[degC]-Mid-S3"]
df4m = df["T[degC]-Mid-S4"]
df5m = df["T[degC]-Mid-S5"]
df6m = df["T[degC]-Mid-S6"]
df7m = df["T[degC]-Mid-S7"]
df8m = df["T[degC]-Mid-S8"]
df9m = df["T[degC]-Mid-S9"]
df10m = df["T[degC]-Mid-S10"]
df11m = df["T[degC]-Mid-S11"]
df12m = df["T[degC]-Mid-S12"]
df13m = df["T[degC]-Mid-S13"]
df14m = df["T[degC]-Mid-S14"]
df15m = df["T[degC]-Mid-S15"]
df16m = df["T[degC]-Mid-S16"]
df17m = df["T[degC]-Mid-S17"]
df18m = df["T[degC]-Mid-S18"]
df19m = df["T[degC]-Mid-S19"]
df20m = df["T[degC]-Mid-S20"]
df21m = df["T[degC]-Mid-S21"]
df22m = df["T[degC]-Mid-S22"]
df23m = df["T[degC]-Mid-S23"]
df24m = df["T[degC]-Mid-S24"]
df25m = df["T[degC]-Mid-S25"]
df26m = df["T[degC]-Mid-S26"]
df27m = df["T[degC]-Mid-S27"]
df28m = df["T[degC]-Mid-S28"]
df29m = df["T[degC]-Mid-S29"]

#High

df1h = df["T[degC]-Top-S1"]
df2h = df["T[degC]-Top-S2"]
df3h = df["T[degC]-Top-S3"]
df4h = df["T[degC]-Top-S4"]
df5h = df["T[degC]-Top-S5"]
df6h = df["T[degC]-Top-S6"]
df7h = df["T[degC]-Top-S7"]
df8h = df["T[degC]-Top-S8"]
df9h = df["T[degC]-Top-S9"]
df10h = df["T[degC]-Top-S10"]
df11h = df["T[degC]-Top-S11"]
df12h = df["T[degC]-Top-S12"]
df13h = df["T[degC]-Top-S13"]
df14h = df["T[degC]-Top-S14"]
df15h = df["T[degC]-Top-S15"]
df16h = df["T[degC]-Top-S16"]
df17h = df["T[degC]-Top-S17"]
df18h = df["T[degC]-Top-S18"]
df19h = df["T[degC]-Top-S19"]
df20h = df["T[degC]-Top-S20"]
df21h = df["T[degC]-Top-S21"]
df22h = df["T[degC]-Top-S22"]
df23h = df["T[degC]-Top-S23"]
df24h = df["T[degC]-Top-S24"]
df25h = df["T[degC]-Top-S25"]
df26h = df["T[degC]-Top-S26"]
df27h = df["T[degC]-Top-S27"]
df28h = df["T[degC]-Top-S28"]
df29h = df["T[degC]-Top-S29"]



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

hours = len(heures_correspondantes(new_times))
print(hours)


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

moyennes = len(moyenne_par_heure(df3))
print(moyennes)


def plot_more_figure(temp, capteurs_groups: list):
    for nb, capteurs in enumerate(capteurs_groups):
        plt.figure()
        for capteur in capteurs:
            plt.plot(heures_correspondantes(temp), moyenne_par_heure(capteur))
            plt.title(f"graph {nb+1}")
            plt.xticks(np.arange(0, 1800, 180), fontsize=5)
    plt.xlabel("Time")
    #plt.xticks(np.arange(0, 1800, 24))
    plt.ylabel("Temperature")
    plt.show()



# new_time représente une liste de temps en heure qui commence à la première heure obtenue, on peut illustrer chacune des courbes des capteurs qui sont tous regrouper dans une liste principale et les différents niveau pour un même capteur (low, med, top) se retrouve dans une nouvelle liste.
# la fonction moyenne_par_heure ne prend pas en compte les premières données, elle commence en même temps que la première heure et effectue la moyenne des données de température, pour en retourner une nouvelle liste
# le tous est illustrer avec la fonction suivante

plot_more_figure(new_times, [[df3, df3m, df3h], [df4, df4m, df4h]])


