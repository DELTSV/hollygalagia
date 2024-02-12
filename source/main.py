import time
import sys

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

# for radars in radarss:
#     for (alpha, gamma) in alphas_gammas:
#         time.sleep(0.5)
#         window = Window(alpha, gamma, radars)
        # time.sleep(0.5)
        # window.setup()
        # time.sleep(0.5)
        # window.run()
        # time.sleep(0.5)
        # plt.plot(window.player.history)
        # plt.show()

alpha = float(sys.argv[1])
gamma = float(sys.argv[2])
radars = []
history = []
for i in range (3, len(sys.argv)):
    tmp = sys.argv[i].split(",")
    radars.append((int(tmp[0]), int(tmp[1])))

while True:
    window = Window(alpha, gamma, radars, history)
    window.setup()
    window.run()
    plt.plot(window.player.history)
    plt.show()