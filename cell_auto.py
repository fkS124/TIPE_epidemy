import pygame as pg
import numpy as np
import matplotlib.pyplot as plt


def simule(prop_dict={
    "I": 0.001,
    "R": 0.1,
    "S": 0.899},
        show_graph=True, auto=False, duree_experience=30):
    pg.init()
    v = pg.math.Vector2

    # PARAMÈTRES D'AFFICHAGE ---------------
    running = True
    screen = pg.display.set_mode((600, 600))
    pg.display.set_caption("Automate Cellulaire")
    dxy = v(0, 0)
    scale = 1.0
    clock = pg.time.Clock()

    # SIMULATION ---------------------------
    simu_en_cours = False
    delai = 100  # en ms
    dernier_refresh = 0
    gene_prop = prop_dict

    # TODO : modifier la durée d'infection !!
    duree_min_infection = 10
    duree_max_infection = 10
    proba_infection = 0.1
    proba_mort = 0.005

    def assigne_etat_initial():
        # assigne aléatoirement un état initial pour une cellule
        x = np.random.rand()
        tot = 0
        for etat, prop in gene_prop.items():
            if tot <= x < tot + prop:
                return etat
            tot += prop
        return "S"

    # GRILLE --------------------------------
    cell_size = 3  # taille d'une cellule
    grid_size = 200  # taille de la grille ex: 200x200
    grid_etat = np.array(
        [[
            assigne_etat_initial()  # état initial
            for _ in range(grid_size)
        ] for _ in range(grid_size)]
    )
    grid_duree_etat = np.array([np.zeros(grid_size) for _ in range(grid_size)])
    update_etat = np.array([np.ones(grid_size) for _ in range(grid_size)])
    liste_infectes = [(x, y) for x in range(grid_size) for y in range(grid_size) if grid_etat[x, y] == "I"]
    colors = {
        "I": (255, 0, 0),  # infecté (I)
        "R": (0, 255, 0),  # immunisé contre la réinffection (R)
        "S": (255, 255, 255),  # susceptible de contracter la maladie (S)
        "M": (0, 0, 0)  # mort (M)
    }
    neighbours = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    def draw_cell(x, y, etat):
        # Pour des raisons de performances, on ne dessine pas à chaque frame chaque cellule
        # on ne dessine que lorsqu'elle change d'état, auquel cas on appelle cette fonction.
        pg.draw.rect(
            screen, colors[etat],
            [
                dxy + cell_size * scale * v(x, y), scale * v(cell_size, cell_size)
            ]
        )

    for x in range(grid_size):
        for y in range(grid_size):
            etat = grid_etat[x, y]
            draw_cell(x, y, etat)

    # Statistiques -------------------
    N_infectes = []
    N_remis = []
    N_mort = []

    if auto:
        simu_en_cours = True
        debut_exp = pg.time.get_ticks()
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    simu_en_cours = not simu_en_cours

        # SIMULATION ----------------
        if simu_en_cours and pg.time.get_ticks() - dernier_refresh > delai:
            # Récupère nla population de chaque catégorie
            unique, counts = np.unique(grid_etat, return_counts=True)
            d = dict(zip(unique, counts))
            N_infectes.append(d["I"] if "I" in d else 0)
            N_remis.append(d["R"] if "R" in d else 0)
            N_mort.append(d["M"] if "M" in d else 0)

            dernier_refresh = pg.time.get_ticks()
            grid_duree_etat += update_etat
            new_liste_infectes = []

            # Mise à jour des infectés
            for x, y in liste_infectes:
                # Temps depuis infection de la cellule
                duree_infection = grid_duree_etat[x, y]
                # Temps d'infection supérieur à la durée de rémission, la cellule se remet
                if duree_infection > duree_max_infection:
                    grid_etat[x, y] = "R"
                    grid_duree_etat[x, y] = 0
                    draw_cell(x, y, "R")
                    continue
                # Probabilité que la cellule meure
                elif np.random.rand() < proba_mort:
                    grid_etat[x, y] = "M"
                    grid_duree_etat[x, y] = 0
                    draw_cell(x, y, "M")
                    continue
                # On garde l'infecté, car il n'est pas mort ni remis
                else:
                    new_liste_infectes.append([x, y])

                # Infection des voisins 
                for dx, dy in neighbours:
                    if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
                        etat_voisin = grid_etat[x + dx, y + dy]
                        # Le voisin en question est susceptible d'être infecté
                        if etat_voisin == "S":
                            # Infection avec une certaine probabilité
                            if np.random.rand() < proba_infection:
                                grid_etat[x + dx, y + dy] = "I"
                                grid_duree_etat[x + dx, y + dy] = 0
                                new_liste_infectes.append([x + dx, y + dy])
                                draw_cell(x + dx, y + dy, "I")
            # Mise à jour de la liste des infectés
            liste_infectes = new_liste_infectes

        if auto:
            if pg.time.get_ticks() - debut_exp > duree_experience * 1000:
                running = False
                break

        clock.tick(30)  # 30 images par seconde
        pg.display.update()

    pg.quit()

    if show_graph:
        plt.grid()
        plt.ylabel("Population")
        plt.xlabel("Temps")
        plt.plot(range(len(N_infectes)), np.array(N_infectes) / (grid_size ** 2), color="red", label="Infectés")
        plt.plot(range(len(N_remis)), np.array(N_remis) / (grid_size ** 2), color="green", label="Remis")
        plt.plot(range(len(N_mort)), np.array(N_mort) / (grid_size ** 2), color="black", label="Mort")
        plt.legend()
        plt.show()

    if auto:
        return [np.array(N_infectes) / (grid_size ** 2),
                np.array(N_remis) / (grid_size ** 2),
                np.array(N_mort) / (grid_size ** 2)]


print(simule(show_graph=False, auto=True))
