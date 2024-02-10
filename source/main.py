import time

from source.ui.Window import Window

import matplotlib.pyplot as plt

radarss = [
    [(-2, 1), (-1, 2), (0, 3), (1, 2), (2, 1)],
    [(-2, 0), (-1, 2), (0, 2), (1, 2), (2, 0), (0, -1)],
    [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
]

alphas_gammas = [
    (1, 1),
    (0.5, 0.5),
    (1.1, 0.8),
    (0.7, 0.9)
]

processes = []

for radars in radarss:
    for (alpha, gamma) in alphas_gammas:
        window = Window(alpha, gamma, radars)
        window.setup()
        time.sleep(0.5)
        window.run()
        plt.plot(window.player.history)
        plt.show()
