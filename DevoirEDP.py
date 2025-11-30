import matplotlib.pyplot as plt
import numpy as np
# initialisation
# bornex
a = -25
b = 25
# borney
c = 0
d = 20
h = 0.1
k = 0.01
m = int((b-a)/h)
n = int((d-c)/k)

# grille
x = np.linspace(a, b, m + 1)
t = np.linspace(c, d, n + 1)

# matrice vide
C = np.zeros((m+1, n+1))

# conditions initiales
for i in range(0, m//2):
    C[i, 0] = 500
for i in range(m//2, m):
    C[i, 0] = 0

# conditions limites
C[0, :] = 500
C[m-1, :] = 0

# coefficients
alpha = 0.4
U = 1
L = 50
    
# resolution
for j in range(0, n):
    for i in range (1, m): 
        C[i, j+1] = (-(4*k*alpha - 2*(h**2))*C[i, j] - U*k*h*(C[i+1, j] 
                                - C[i-1, j]) + 2*k*alpha*(C[i-1, j] + C[i+1, j]))/(2*(h**2))

#condition de stabilité
r = alpha*k/(h**2)
print(r)

#Concentration à certains temps
t1= int(5.0/k)
t2= int(10.0/k)
t3= int(0.0/k)

# figure
plt.plot(x, C[:, t1], label='5 sec', color='b')
plt.plot(x, C[:, t2], label='10 sec', color='r')
plt.plot(x, C[:, t3], label='0 sec', color='g')
plt.title('Évolution de la concentration à t = 0, 5 et 10 secondes')
plt.xlabel('x (m)')
plt.ylabel('Concentration (ppm)')
plt.legend()


