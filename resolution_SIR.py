import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


class GrapheDynamique:

    def __init__(self):
        # Création de la fenêtre
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)

        # Initialisation du solveur
        self.solveur = SolveurSIR()

        # Créer les boîte de texte pour toutes les variables
        self.textboxS = CoeffTextBox(self, [0.2, 0.20, 0.1, 0.04], "S0 ",
                                     self.solveur.DEFAULT_S0, self.solveur, "s0")
        self.textboxI = CoeffTextBox(self, [0.2, 0.15, 0.1, 0.04], "I0 ",
                                     self.solveur.DEFAULT_I0, self.solveur, "i0")
        self.textboxR = CoeffTextBox(self, [0.2, 0.10, 0.1, 0.04], "R0 ",
                                     self.solveur.DEFAULT_R0, self.solveur, "r0")
        self.textboxD = CoeffTextBox(self, [0.2, 0.05, 0.1, 0.04], "M0 ",
                                     self.solveur.DEFAULT_M0, self.solveur, "m0")
        self.textboxBeta = CoeffTextBox(self, [0.45, 0.20, 0.1, 0.04], "Beta ",
                                        self.solveur.DEFAULT_BETA, self.solveur, "beta")
        self.textboxGamma = CoeffTextBox(self, [0.45, 0.15, 0.1, 0.04], "Gamma ",
                                         self.solveur.DEFAULT_GAMMA, self.solveur, "gamma")
        self.textboxDelta = CoeffTextBox(self, [0.45, 0.10, 0.1, 0.04], "Delta ",
                                         self.solveur.DEFAULT_DELTA, self.solveur, "delta")
        self.textboxDeltaT = CoeffTextBox(self, [0.75, 0.20, 0.1, 0.04], "Durée exp ",
                                          self.solveur.stop, self.solveur, "stop")
        self.textboxResolution = CoeffTextBox(self, [0.75, 0.15, 0.1, 0.04], "Résolution ",
                                              self.solveur.n_points, self.solveur, "n_points")

        self.lS, = self.ax.plot(self.solveur.t, self.solveur.s, label="Susceptible")
        self.lI, = self.ax.plot(self.solveur.t, self.solveur.i, label="Infectés")
        self.lR, = self.ax.plot(self.solveur.t, self.solveur.r, label="Remis")
        self.lM, = self.ax.plot(self.solveur.t, self.solveur.m, label="Morts")

        self.update_courbes()

    def update_courbes(self):
        # Mets à jour toutes les courbes avec les nouvelles données
        self.lS.set_xdata(self.solveur.t)
        self.lS.set_ydata(self.solveur.s)
        self.lI.set_xdata(self.solveur.t)
        self.lI.set_ydata(self.solveur.i)
        self.lR.set_xdata(self.solveur.t)
        self.lR.set_ydata(self.solveur.r)
        self.lM.set_xdata(self.solveur.t)
        self.lM.set_ydata(self.solveur.m)

        # Mets à jour l'échelle et la fenêtre
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

    def show(self):
        # Affiche une grille en fond
        self.ax.grid()
        # Affiche la légende
        self.ax.legend()
        # Lance l'application
        plt.show()


class SolveurSIR:

    # Définir les paramètres
    DEFAULT_BETA = 0.3  # Taux de transmission
    DEFAULT_GAMMA = 0.1  # Taux de récupération
    DEFAULT_DELTA = 0.01  # Taux de décès

    # Conditions initiales
    DEFAULT_S0 = 0.899  # Population initialement susceptible d'être infectée
    DEFAULT_I0 = 0.001  # Population initialement infectée
    DEFAULT_R0 = 0.1  # Population initialement retirée
    DEFAULT_M0 = 0  # Population initialement morte

    def __init__(self):

        # Paramètres de temps
        self.start, self.stop, self.n_points = 0, 200, 1000

        # Caractéristiques de l'épidémie
        self.s0, self.i0, self.r0, self.m0 = (self.DEFAULT_S0, self.DEFAULT_I0,
                                              self.DEFAULT_R0, self.DEFAULT_M0)
        self.beta, self.gamma, self.delta = self.DEFAULT_BETA, self.DEFAULT_GAMMA, self.DEFAULT_DELTA

        # Courbes des différentes classes
        self.s, self.i, self.r, self.m = tuple([np.array([])]*4)  # ordonnées
        self.t = np.linspace(self.start, self.stop, self.n_points)

        # On remplit les listes en résolvant le système avec les valeurs par défaut
        self.solve_equation()

    @staticmethod
    def deriv(y, t, beta, gamma, delta):
        # Fonction décrivant le système d'équations différentielles
        S, I, R, M = y
        dSdt = -beta * S * I
        dIdt = beta * S * I - gamma * I - delta * I
        dRdt = gamma * I
        dMdt = delta * I
        return [dSdt, dIdt, dRdt, dMdt]

    def solve_equation(self):
        # Temps
        self.t = np.linspace(int(self.start), int(self.stop), int(self.n_points))

        # Conditions initiales regroupées
        y0 = [self.s0, self.i0, self.r0, self.m0]

        # Résoudre les équations différentielles
        solution = odeint(self.deriv, y0, self.t, args=(self.beta, self.gamma, self.delta))

        # On met à jour les ordonnées
        self.s = solution[:, 0]
        self.i = solution[:, 1]
        self.r = solution[:, 2]
        self.m = solution[:, 3]


class CoeffTextBox(TextBox):

    def __init__(self,
                 graphe: GrapheDynamique,
                 coordinates: list[float],
                 label: str,
                 default: float,
                 solveur: SolveurSIR,
                 var: str):
        # On initialise la classe parente
        super().__init__(plt.axes(coordinates), label, initial=str(default))
        super().on_submit(self.update_value)

        # Récupération de l'addresse du solveur
        self.solveur = solveur
        # Récupération du nom de la variable à changer
        self.var = var
        # Récupération du graphe pour les mises à jour
        self.graphe = graphe

    def update_value(self, text):
        try:
            value = float(text)
            setattr(self.solveur, self.var, value)
            self.solveur.solve_equation()
            self.graphe.update_courbes()
        except ValueError:
            print("Illegal value entered.")


if __name__ == '__main__':
    grapheDy = GrapheDynamique()
    grapheDy.show()