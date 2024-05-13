import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dxy_transmission = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 1),
                    (1, -1), (1, 0), (1, 1)]

default_epidemy = {
    "S": 0.999,  # Prop initiale de Susceptibles d'être infectés
    "I": 0.001,  # Prop initiale d'Infectés
    "R": 0.0,  # Prop initiale d'insensibles à la Réinfection
    "D": 0.0,  # Prop initiale de mort (Dead)
    "beta": 0.1,  # Taux de transmission
    "gamma": 0.3,  # Taux de récupération
    "delta": 0.01  # Taux de décès
}


def simule(epidemy: dict[str, float], size: int = 200, iterations: int = 10) -> list[np.array]:
    all_etats = []
    # 0 = S, 1 = I, 2 = R, 3 = D (mort)
    grid_etat = np.zeros((size, size))
    # Initialisation des états initiaux
    for x in range(size):
        for y in range(size):
            grid_etat[x, y] = np.random.choice(range(4), p=[epidemy["S"], epidemy["I"], epidemy["R"], epidemy["D"]])

    print("Début de la simulation : ", epidemy)

    # Simulation sur N iterations
    for i in range(iterations):
        # Enregistrement de la frame précédente
        all_etats.append(grid_etat.copy())
        # Création de la nouvelle frame à partir de la précédente
        new_grid_etat = grid_etat.copy()
        # Parcours de la nouvelle frame pour la mettre à jour
        for x in range(size):
            for y in range(size):
                # Récupération de l'état en (x, y)
                etat = grid_etat[x, y]
                # Cellule infectée
                if etat == 1:
                    # La cellule a une certaine chance de se remettre
                    remission = np.random.rand()
                    if remission < epidemy["gamma"]:
                        new_grid_etat[x, y] = 2

                    # La cellule a une certaine chance de mourir
                    deces = np.random.rand()
                    if deces < epidemy["delta"]:
                        new_grid_etat[x, y] = 3

                    # La cellule propage la maladie autour d'elle
                    for dx, dy in dxy_transmission:
                        # Vérification que la cellule ne se trouve pas sur un bord
                        if not (0 <= x + dx < size and 0 <= y + dy < size):
                            continue
                        # Récupération de l'état de la cellule cible
                        etat_cible = grid_etat[x + dx, y + dy]
                        # Si la cellule n'est pas susceptible on passe à l'iter suivante
                        if etat_cible != 0:
                            continue
                        # Calcul de la chance de contamination
                        contamination = np.random.rand()
                        if contamination < epidemy["beta"] and new_grid_etat[x + dx, y + dy] == 0:
                            new_grid_etat[x + dx, y + dy] = 1

        grid_etat = new_grid_etat.copy()
        # calcul de l'itération suivante

    print("Fin de la simulation : ", epidemy)

    return all_etats


def animate(liste_etats):
    # Couleurs associées à chaque chiffre
    colors = [(0, 1, 0), (1, 0, 0), (0, 0, 1), 'black']

    # Fonction d'animation pour afficher chaque tableau avec la couleur correspondante
    def animate_frame(i):
        plt.clf()  # Effacer le graphique précédent
        plt.imshow(liste_etats[i], cmap=plt.cm.colors.ListedColormap(colors))
        plt.title(f"Itération n°{i + 1}/{len(liste_etats)}")
        plt.axis('off')  # Désactiver les axes

    # Créer l'animation
    fig = plt.figure()
    anim = FuncAnimation(fig, animate_frame, frames=len(liste_etats), interval=200)

    plt.show()


if __name__ == "__main__":
    animate(simule(default_epidemy, size=100, iterations=50))
