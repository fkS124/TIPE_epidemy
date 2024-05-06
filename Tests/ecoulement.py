import numpy as np
import matplotlib.pyplot as plt

# Paramètres
L = 2.0  # Longueur de la boîte
N = 50   # Nombre de points sur chaque axe
h = L / N  # Espacement entre les points
x = np.linspace(-L/2, L/2, N)
y = np.linspace(-L/2, L/2, N)
X, Y = np.meshgrid(x, y)

# Position et rayon de la sphère
R = 0.5  # Rayon de la sphère
Xc, Yc = 0, 0  # Position du centre de la sphère

# Fonction pour calculer la vitesse du fluide autour de la sphère
def calculate_velocity(X, Y, Xc, Yc, R, v_inf):
    # Coordonnées polaires
    r = np.sqrt((X - Xc)**2 + (Y - Yc)**2)
    theta = np.arctan2(Y - Yc, X - Xc)
    # Vitesse du fluide
    Vx = v_inf * (1 - R**2 / r**2) * np.cos(theta)
    Vy = v_inf * (1 - R**2 / r**2) * np.sin(theta)
    return Vx, Vy

# Vitesse à l'infini
v_inf = 1.0

# Calcul de la vitesse du fluide
Vx, Vy = calculate_velocity(X, Y, Xc, Yc, R, v_inf)

# Affichage du champ de vitesse
plt.figure(figsize=(8, 6))
plt.streamplot(X, Y, Vx, Vy, density=2, arrowsize=2)
plt.gca().set_aspect('equal', adjustable='box')
plt.title('Écoulement laminaire autour d\'une sphère')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-L/2, L/2)
plt.ylim(-L/2, L/2)
plt.scatter(Xc, Yc, color='red', marker='o', label='Sphère')
plt.legend()
plt.grid(True)
plt.show()