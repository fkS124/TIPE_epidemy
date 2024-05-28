from cell_auto_v2 import simule
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from typing import Any
import numpy as np


def generer_epidemies(N: int, consts: list[float | None],
                      starts: tuple = (0, 0, 0, 0, 0, 0),
                      stops: tuple = (1, 1, 1, 1, 1, 1)) -> list[dict[str, float]]:

    # Création des N points entre 0 et 1
    Lpoints = [np.linspace(start, stop, N) for start, stop in zip(starts, stops)]

    # On récupère le nombre de valeurs à faire varier
    n = consts.count(None)

    # On génère une grille à n dimensions, pour générer tous les n-uplets entre 0 et 1
    n_uplets = np.meshgrid(*([points for i, points in enumerate(Lpoints) if consts[i] is None]), indexing='ij')

    # On les réorganise pour qu'ils forment une liste de n-uplets
    n_uplets = np.column_stack([n_uplets[i].ravel() for i in range(n)])

    # On réinsère les constantes pour former les six-uplets
    indice_n_uplet = 0  # Correspond à la colonne que l'on récupère
    colonnes = []
    for const in consts:
        # Si c'est None, alors on a fait varier la valeur donc on récupère une colonne des n_uplets
        if const is None:
            colonnes.append(n_uplets[:, indice_n_uplet])
            indice_n_uplet += 1
        # Sinon on crée une colonne de la même taille, contenant uniquement la constante voulue
        else:
            colonnes.append(np.array([const]*len(n_uplets)))
    sixuplets = np.column_stack(colonnes)

    # Génération des dictionnaires
    L_epidemies = [
        {
            "S": s,
            "I": i,
            "R": r,
            "D": 0,
            "delta": d,
            "beta": b,
            "gamma": g
        } for s, i, r, d, b, g in sixuplets if np.isclose(s + i + r, 1)
    ]

    return L_epidemies


def traitement_resultats(resultats: list[dict]) -> dict[str, Any]:

    stats = {"I0": [], "R0": [], "n_maladie_contractee": [], "n_morts": [], "beta": [], "gamma": []}
    for resultat in resultats:
        # Nombre d'infectés initialement
        stats["I0"].append(resultat["epidemy"]["I"])
        # Nombre d'immunisés initialement
        stats["R0"].append(resultat["epidemy"]["R"])
        # Taux de transmission beta
        stats["beta"].append(resultat["epidemy"]["beta"])
        # Taux de récupération gamma
        stats["gamma"].append(resultat["epidemy"]["gamma"])

        # Dernier état de la simulation
        derniere_iteration = resultat["sim_result"][-1]
        # Comptage du total de personnes ayant contracté la maladie
        stats["n_maladie_contractee"].append(np.count_nonzero(derniere_iteration) / resultat["size"] ** 2)
        # Compte du nombre de morts
        stats["n_morts"].append(np.count_nonzero(derniere_iteration == 3) / resultat["size"] ** 2)

    return stats


def graphe_resultats(stats: dict[str, float]) -> None:

    # plt.scatter(stats["beta"], stats["n_maladie_contractee"], label="Nombre d'infections", color="green")
    # plt.xlabel("beta (taux de transmission)")
    # plt.ylabel("Nombre d'infections")
    # plt.grid()
    # plt.legend()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    #
    # ax.plot_trisurf(stats["beta"], stats["gamma"], stats["n_maladie_contractee"])
    #
    # ax.set_xlabel("beta (taux de transmission)")
    # ax.set_ylabel("gamma (taux de récupération)")
    # ax.set_zlabel("Nombre d'infections")

    # plt.scatter(stats["beta"], stats["gamma"], c=stats["n_maladie_contractee"], cmap='inferno', s=100)
    # plt.colorbar()
    # plt.xlabel('beta')
    # plt.ylabel('gamma')
    # plt.title(f"Nombre final d'inféctés (I0={round(stats['I0'][0], 2)})")

    # ------ Percolation 3D --------
    # # Récupération des données
    # x, y, z = stats["beta"], stats["gamma"], stats["n_maladie_contractee"]
    #
    # # Créer une grille régulière de points à partir des données aléatoires
    # grid_x, grid_y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    #
    # # Interpoler les valeurs z pour créer une surface régulière
    # grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
    #
    # # Créer la figure et l'axe 3D
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # # Créer une surface 3D avec la colormap
    # surface = ax.plot_surface(grid_x, grid_y, grid_z, facecolors=plt.cm.viridis(grid_z), rstride=1, cstride=1,
    #                           antialiased=True)
    #
    # # Ajouter une barre de couleur
    # cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), ax=ax, shrink=0.5, aspect=5)
    # cbar.set_label("Nombre final d'infections")
    #
    # # Ajouter des étiquettes aux axes
    # ax.set_xlabel('beta')
    # ax.set_ylabel('gamma')
    # ax.set_zlabel("Nombre final d'infections")
    #
    # # Afficher le graphique
    # plt.show()

    plt.plot(stats["R0"], np.array(stats["n_maladie_contractee"])-np.array(stats["R0"]), color="red")
    plt.grid()
    plt.xlabel("Nombre initial de vaccinés")
    plt.ylabel("Nombre final d'infectés")
    plt.show()


def simulations(N: int, size: int = 100, iterations: int = 40) -> None:
    # Générations des différentes caractéristiques d'épidémies
    # consts = [S0, I0, R0, D0, delta, beta, gamma]
    L_epidemies = generer_epidemies(
        N, consts=[None, 0.01, None, 0, 0.144, 0.045],
        starts=(0, 0, 0, 0, 0, 0),
        stops=(0.99, 1, 0.99, 1, 1, 1)
    )

    # Simulation et formatage des résultats
    resultats = [{
        "sim_result": simule(epidemy, size, iterations),
        "epidemy": epidemy,
        "size": size,
        "iterations": iterations
    } for epidemy in L_epidemies]

    # Analyse des résultats bruts
    analyse = traitement_resultats(resultats)

    # Graphe des résultats
    graphe_resultats(analyse)


if __name__ == "__main__":
    # epidemies = generer_epidemies(step=0.1, consts=[None, None, .0, .01, .5, .3])
    # print(epidemies)

    simulations(200, iterations=30)
