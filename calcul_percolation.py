from cell_auto_v2 import simule
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import Any
import numpy as np


def generate_epidemies(N: int, consts: list[float | None], start: float = 0.0,
                       stop: float = 1.0) -> list[dict[str, float]]:
    # Création des N points entre 0 et 1
    points = np.linspace(start, stop, N)
    # On récupère le nombre de valeurs à faire varier
    n = consts.count(None)
    # On génère une grille à n dimensions, pour générer tous les n-uplets entre 0 et 1
    n_uplets = np.meshgrid(*([points]*n), indexing='ij')
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
    stats = {"I0": [], "n_maladie_contractee": [], "n_morts": [], "beta": [], "gamma": []}
    for resultat in resultats:
        # Nombre d'infectés initialement
        stats["I0"].append(resultat["epidemy"]["I"])
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

    plt.scatter(stats["beta"], stats["gamma"], c=stats["n_maladie_contractee"], cmap='inferno', s=100)
    plt.colorbar()
    plt.xlabel('beta')
    plt.ylabel('gamma')
    plt.title("Nombre total d'inféctés")

    plt.show()


def simulations(N, size=100, iterations=40):
    # Générations des différentes caractéristiques d'épidémies
    L_epidemies = generate_epidemies(N, consts=[0.5, 0.5, .0, 0.01, None, None], start=0.00, stop=1.0)

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
    # epidemies = generate_epidemies(step=0.1, consts=[None, None, .0, .01, .5, .3])
    # print(epidemies)

    simulations(20)
