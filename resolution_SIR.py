import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Définir le graphe
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

# Définir les paramètres
beta = 0.3  # Taux de transmission
gamma = 0.1  # Taux de récupération
delta = 0.01  # Taux de décès

# Conditions initiales
S0 = 0.899  # Population initialement susceptible
I0 = 0.001  # Population initialement infectée
R0 = 0.1  # Population initialement retirée
M0 = 0  # Population initialement morte


# Définir le système d'équations différentielles
def deriv(y, t, beta, gamma, delta):
    S, I, R, M = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I - delta * I
    dRdt = gamma * I
    dMdt = delta * I
    return [dSdt, dIdt, dRdt, dMdt]


# Temps
t = np.linspace(0, 200, 1000)

# Conditions initiales regroupées
y0 = [S0, I0, R0, M0]

# Résoudre les équations différentielles
solution = odeint(deriv, y0, t, args=(beta, gamma, delta))

# Tracer les résultats
lS, = ax.plot(t, solution[:, 0], label='Susceptible')
lI, = ax.plot(t, solution[:, 1], label='Infecté')
lR, = ax.plot(t, solution[:, 2], label='Retiré')
lM, = ax.plot(t, solution[:, 3], label='Mort')

plt.grid()
plt.xlabel('Temps')
plt.ylabel('Population')
plt.legend()

# Initialisation de l'interface utilisateur

ax_slider_S = plt.axes([0.10, 0.15, 0.30, 0.03])
slider_S = Slider(ax_slider_S, 'S0', 0, 1, valinit=S0)

ax_slider_R = plt.axes([0.10, 0.10, 0.30, 0.03])
slider_R = Slider(ax_slider_R, 'R0', 0, 1, valinit=R0)

ax_slider_I = plt.axes([0.10, 0.05, 0.30, 0.03])
slider_I = Slider(ax_slider_I, 'I0', 0, 1, valinit=I0)

ax_slider_gamma = plt.axes([0.60, 0.05, 0.30, 0.03])
slider_gamma = Slider(ax_slider_gamma, 'gamma', 0, 1, valinit=gamma)

ax_slider_beta = plt.axes([0.60, 0.10, 0.30, 0.03])
slider_beta = Slider(ax_slider_beta, 'beta', 0, 1, valinit=beta)

ax_slider_delta = plt.axes([0.60, 0.15, 0.30, 0.03])
slider_delta = Slider(ax_slider_delta, 'delta', 0, 0.1, valinit=delta)


def normalize_variables(var1, var2, var3):
    """
    L'objectif de cette fonction est d'imposer var1,
    et de changer var2 et var3 pour imposer var1 + var2 + var3 = 1
    """
    """dvar = (var1 - (1 - var2 - var3)) / 2
    var2 -= dvar
    var3 -= dvar
    if var2 < 0:
        var3 += var2
        var2 = 0
    elif var3 < 0:
        var2 += var3
        var3 = 0"""
    return var1, var2, var3


def update_all_slider(S, I, R):
    slider_S.eventson = False
    slider_I.eventson = False
    slider_R.eventson = False
    slider_S.set_val(S)
    slider_I.set_val(I)
    slider_R.set_val(R)
    slider_S.eventson = True
    slider_I.eventson = True
    slider_R.eventson = True


def update_beta(val):
    global beta
    beta = val
    solve_equation()


def update_gamma(val):
    global gamma
    gamma = val
    solve_equation()


def update_delta(val):
    global delta
    delta = val
    solve_equation()


def update_S0(val):
    global S0, I0, R0
    S0, I0, R0 = normalize_variables(val, I0, R0)
    update_all_slider(S0, I0, R0)
    solve_equation()


def update_I0(val):
    global S0, I0, R0
    I0, R0, S0 = normalize_variables(val, R0, S0)
    update_all_slider(S0, I0, R0)
    solve_equation()


def update_R0(val):
    global S0, I0, R0
    R0, I0, S0 = normalize_variables(val, I0, S0)
    update_all_slider(S0, I0, R0)
    solve_equation()


def solve_equation():
    # Temps
    t = np.linspace(0, 200, 1000)

    # Conditions initiales regroupées
    y0 = [S0, I0, R0, M0]

    # Résoudre les équations différentielles
    solution = odeint(deriv, y0, t, args=(beta, gamma, delta))

    # Mettre à jour les valeurs sur le graphe
    lS.set_ydata(solution[:, 0])
    lI.set_ydata(solution[:, 1])
    lR.set_ydata(solution[:, 2])
    lM.set_ydata(solution[:, 3])
    fig.canvas.draw_idle()


# Assignation des fonctions de miser à jour
slider_S.on_changed(update_S0)
slider_R.on_changed(update_R0)
slider_I.on_changed(update_I0)
slider_gamma.on_changed(update_gamma)
slider_beta.on_changed(update_beta)
slider_delta.on_changed(update_delta)

plt.show()
