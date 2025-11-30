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
plt.axvline(x=20, ymin=0, ymax=10, linewidth=3, linestyle="--", color='black')
plt.show()




##################################version qui marche 

## Graphique de temperature par niveau pour le plateau 1 vs plateau 2
liste_niveau = ['Low','Mid','Top']

# faire plusieurs figure de plateau a cote
f, axs = plt.subplots(2, 1,figsize=(10,7), sharex=True)

for n, level in enumerate(plateau_1):
    # calcul de la moyenne des capteurs
    moy_plateau = np.nanmean(level, axis=1)
    axs[0].plot(np.arange(len(moy_plateau)), moy_plateau, label=liste_niveau[n], zorder=0)

axs[0].axvline(x=20000, ymin=5, ymax=55, linewidth=43, linestyle="--", color='black',zorder=1)
axs[0].set_title('Évolution de la température sous le plateau 1 \n moyenne de capteurs par niveau')
axs[0].set_ylabel('Température [$^\circ$C]')
# ax1.set_xlabel('Temps [2min]')
axs[0].legend()


for n, level in enumerate(plateau_2):
    # calcul de la moyenne des capteurs
    moy_plateau = np.nanmean(level, axis=1)
    axs[1].plot(np.arange(len(moy_plateau)), moy_plateau, label=liste_niveau[n], zorder=0)

axs[1].axvline(x=20000, ymin=5, ymax=55, linewidth=43, linestyle="--", color='black',zorder=1)
# ax2.set_title('Évolution de la température sous le plateau 1 \n moyenne de capteurs par niveau')
axs[1].set_ylabel('Température [$^\circ$C]')
# ax2.set_xlabel('Temps [2min]')
axs[1].legend()

plt.show()
