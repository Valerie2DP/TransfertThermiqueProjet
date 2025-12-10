import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc
import os

# Supprimer les anciens graphiques
if os.path.exists('T2_vs_temps.png'):
    os.remove('T2_vs_temps.png')

gc.collect()

# Paramètres physiques
Long = 26.1  # m
larg = 3.7   # m
Haut = 1.7   # m

unite1 = Long / 32
unite2 = larg / 4

cp = 1007  # J/kgK
e_dalle = 18 / 1000  # m
A_section = larg * Long / 3
e_beton = 0.4

A_mur12 = Haut * (20 * unite1 + 10 * unite2)
A_mur34 = Haut * (22 * unite1 + 8 * unite2)
A_mur56 = Haut * (22 * unite1 + 10 * unite2)

k_beton = 1.8  # W/mK
h_air = 10     # W/m2K

k_asph = 1.0   # W/mK
k_acier = 50   # W/mK
k_dalle = (8 * k_asph + 10 * k_acier) / 18

C_vol = 2300 * 880  # J/m3K
C = C_vol * e_dalle * A_section  # J/K

# Débit d'air
gap12 = 0.04107
gap23 = 0.01930
gap34 = -0.06402
gap45 = -0.05980
gap56 = -0.03247
gap1 = 0.04483
gap6 = 0.02567

# Chaleur
q_heater_r = 10000  # W
q_heater_b = 7500   # W

# Initialisation
dt = 3600
nt = 1800

data = pd.read_csv('nouveau_fichier_de_données_en_heure.csv')
T_ext = data['Outdoor temperature [deg. C]'].values

T2 = np.zeros((nt - 1, 3))  # matrice T2 t
T3 = np.zeros((nt - 1, 3))  # matrice T3 t

# Système matriciel
T = np.zeros((nt - 1, 9))

# Initialiser T avec une température de départ (20°C)
for i in range(9):
    T[0, i] = 35
    T[1, i] = 35

# Résolution
for t in range(2, nt - 1):

    # Calculer les résistances à chaque itération
    Rcond = e_dalle / (k_dalle * A_section)
    Rconv = 1 / (h_air * A_section)

    R_beton1 = e_beton / (k_beton * A_mur12)
    R_beton2 = e_beton / (k_beton * A_mur34)
    R_beton3 = e_beton / (k_beton * A_mur56)

    Req1 = R_beton1 + 1 / (h_air * A_mur12)
    Req2 = R_beton2 + 1 / (h_air * A_mur34)
    Req3 = R_beton3 + 1 / (h_air * A_mur56)

    if T_ext[t] < 5:
        q12 = q_heater_r + 2 * q_heater_b
        q34 = q_heater_r + q_heater_b
        q56 = q_heater_r + q_heater_b

        a12 = 0.2381
        a21 = 0.4438
        a23 = 0.3268
        a32 = 0.7042
        a34 = 0.2646
        a43 = 0.5915
        a45 = 0.1988
        a54 = 0.2915
        a56 = 0.4694
        a65 = 0.4070

        A = np.array([
            [((1 / Rconv) + (1 / Rcond)), -1 / Rconv, 0, 0, 0, 0, 0, 0, 0],  # Noeud 11
            [1 / Rconv,
             -((1 / Req1) + (1 / Rconv)) - cp * (a23 + a32 + (gap1 + gap12 + gap23 / 2)),
             1 / Req1,
             cp * (a23 + a32),
             0, 0, 0, 0, 0],  # Noeud 12
            [0,
             -1 / Req1,
             ((C / dt) + (1 / Req1)),
             0, 0, 0, 0, 0, 0],  # Noeud 13
            [0, 0, 0,
             ((1 / Rconv) + (1 / Rcond)),
             -1 / Rconv,
             0, 0, 0, 0],  # Noeud 21
            [0,
             cp * (a32 + a23),
             0,
             1 / Rconv,
             -((1 / Req2) + (1 / Rconv)) - cp * (a32 + a23 + a45 + a54 + (gap23 / 2 + gap34 + gap45 / 2)),
             1 / Req2,
             0,
             cp * (a45 + a54),
             0],  # Noeud 22
            [0, 0, 0,
             0,
             -1 / Req2,
             ((C / dt) + (1 / Req2)),
             0, 0, 0],  # Noeud 23
            [0, 0, 0, 0, 0, 0,
             ((1 / Rconv) + (1 / Rcond)),
             -1 / Rconv,
             0],  # Noeud 31
            [0, 0, 0, 0,
             cp * (a45 + a54),
             0,
             1 / Rconv,
             -((1 / Req3) + (1 / Rconv)) - cp * (a45 + a54 + (gap45 / 2 + gap56 + gap6)),
             1 / Req3],  # Noeud 32
            [0, 0, 0, 0, 0, 0,
             0,
             -1 / Req3,
             ((C / dt) + (1 / Req3))]  # Noeud 33
        ], dtype=float)

        B = np.array([
            T_ext[t] / Rcond,
            -q12 - cp * (gap12 + gap23 / 2 + gap1) * T_ext[t],
            C * T[t - 1, 2] / dt,
            T_ext[t] / Rcond,
            -q34 - (gap23 / 2 + gap34 + gap45 / 2) * cp * T_ext[t],
            C * T[t - 1, 5] / dt,
            T_ext[t] / Rcond,
            -q56 - (gap45 / 2 + gap56 + gap6) * cp * T_ext[t],
            C * T[t - 1, 8] / dt
        ]).reshape(-1, 1)

    else:
        q12 = 0
        q34 = 0
        q56 = 0

        a12 = 0.04113
        a21 = 0.06844
        a23 = 0.05290
        a32 = 0.09304
        a34 = 0.05121
        a43 = 0.10386
        a45 = 0.04163
        a54 = 0.08528
        a56 = 0.03718
        a65 = 0.05788

        A = np.array([
            [((1 / Rconv) + (1 / Rcond)), -1 / Rconv, 0, 0, 0, 0, 0, 0, 0],  # Noeud 11
            [1 / Rconv,
             -((1 / Req1) + (1 / Rconv)) - cp * (a23 + a32 + (gap1 + gap12 + gap23 / 2)),
             1 / Req1,
             cp * (a23 + a32),
             0, 0, 0, 0, 0],  # Noeud 12
            [0,
             -1 / Req1,
             ((C / dt) + (1 / Req1)),
             0, 0, 0, 0, 0, 0],  # Noeud 13
            [0, 0, 0,
             ((1 / Rconv) + (1 / Rcond)),
             -1 / Rconv,
             0, 0, 0, 0],  # Noeud 21
            [0,
             cp * (a32 + a23),
             0,
             1 / Rconv,
             -((1 / Req2) + (1 / Rconv)) - cp * (a32 + a23 + a45 + a54 + (gap23 / 2 + gap34 + gap45 / 2)),
             1 / Req2,
             0,
             cp * (a45 + a54),
             0],  # Noeud 22
            [0, 0, 0,
             0,
             -1 / Req2,
             ((C / dt) + (1 / Req2)),
             0, 0, 0],  # Noeud 23
            [0, 0, 0, 0, 0, 0,
             ((1 / Rconv) + (1 / Rcond)),
             -1 / Rconv,
             0],  # Noeud 31
            [0, 0, 0, 0,
             cp * (a45 + a54),
             0,
             1 / Rconv,
             -((1 / Req3) + (1 / Rconv)) - cp * (a45 + a54 + (gap45 / 2 + gap56 + gap6)),
             1 / Req3],  # Noeud 32
            [0, 0, 0, 0, 0, 0,
             0,
             -1 / Req3,
             ((C / dt) + (1 / Req3))]  # Noeud 33
        ], dtype=float)

        B = np.array([
            T_ext[t] / Rcond,
            -q12 - cp * (gap12 + gap23 / 2 + gap1) * T_ext[t],
            C * T[t - 1, 2] / dt,
            T_ext[t] / Rcond,
            -q34 - (gap23 / 2 + gap34 + gap45 / 2) * cp * T_ext[t],
            C * T[t - 1, 5] / dt,
            T_ext[t] / Rcond,
            -q56 - (gap45 / 2 + gap56 + gap6) * cp * T_ext[t],
            C * T[t - 1, 8] / dt
        ]).reshape(-1, 1)

    # Résolution du système
    T_result = np.linalg.solve(A, B)

    for i in range(9):
        T[t, i] = T_result[i, 0]

    n = t - 2
    T2[n, 0] = T[t, 1]  # T12
    T2[n, 1] = T[t, 4]  # T22
    T2[n, 2] = T[t, 7]  # T32

    T3[n, 0] = T[t, 2]  # T13
    T3[n, 1] = T[t, 5]  # T23
    T3[n, 2] = T[t, 8]  # T33

# Ne pas afficher les grandes matrices en console pour obtenir seulement le graphique

# Graphique de T2 en fonction du temps
print("Création du graphique T2...")
temps_heures = np.arange(len(T2))

plt.figure(figsize=(12, 6))
plt.plot(temps_heures, T2[:, 0], label='T12 (zone 1)', linewidth=2)
plt.plot(temps_heures, T2[:, 1], label='T22 (zone 2)', linewidth=2)
plt.plot(temps_heures, T2[:, 2], label='T32 (zone 3)', linewidth=2)

plt.xlabel('Temps (heures)')
plt.ylabel('Température (°C)')
plt.title("Évolution de la température T2 en fonction du temps")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('T2_vs_temps.png', dpi=150)
print("Graphique T2 sauvegardé en tant que 'T2_vs_temps.png'")