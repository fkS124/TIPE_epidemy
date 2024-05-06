import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np



amp = 1.0
freq = 1.0

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

t = np.linspace(0, 2 * np.pi, 100)
s = amp * np.sin(2* np.pi * freq * t)
l, = ax.plot(t, s, lw=2)

ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor="red")
slider = Slider(ax_slider, 'Frequency', 0.1, 0.5, valinit=freq)


def update(value):
    freq = slider.val
    l.set_ydata(amp * np.sin(2 * np.pi * freq * t))
    fig.canvas.draw_idle()


slider.on_changed(update)


ax_slider2 = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor="red")
slider2 = Slider(ax_slider2, 'Amplitude', 1, 5, valinit=amp) 

def update2(value):
    amp = slider2.val
    l.set_ydata(amp * np.sin(2 * np.pi * freq * t))
    fig.canvas.draw_idle()

slider2.on_changed(update2)


plt.show()


# https://www.youtube.com/watch?v=p-xJsc6LSx0
# Other UI 