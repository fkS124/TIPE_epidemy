import numpy as np
import matplotlib.pyplot as plt 

# Définir la plage de valeurs pour chaque dimension
valeurs_x = np.linspace(0, 10, 4)  # 5 valeurs entre 0 et 10
valeurs_y = np.linspace(0, 20, 3)  # 8 valeurs entre 0 et 20

# Créer une grille bidimensionnelle
grille_x, grille_y = np.meshgrid(valeurs_x, valeurs_y)

print(grille_x)
print(grille_y)

# Voir les résultats
plt.scatter(grille_x, grille_y)
plt.show()