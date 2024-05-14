import matplotlib.pyplot as plt

# Exemple de données
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 35]

# Tracer le graphique
plt.plot(x, y)

# Définir les nouvelles valeurs de l'axe des x et des étiquettes
nouvelles_valeurs_x = [1, 2, 3, 4, 5]
nouvelles_etiquettes_x = ['a', 'b', 'c', 'd', 'e']

# Changer les valeurs et les étiquettes de l'axe des x
plt.gca().set_xticks(nouvelles_valeurs_x)
plt.gca().set_xticklabels(nouvelles_etiquettes_x)

# Afficher le graphique
plt.show()