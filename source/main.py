from source.ui.Window import Window

radarss = [
    [(-2, 1), (-1, 2), (0, 3), (1, 2), (2, 1)],
    [(-2, 0), (-1, 2), (0, 2), (1, 2), (2, 0), (0, -1)]
]

alphas_gammas = [
    (1.1, 0.8)
]

processes = []

for radars in radarss:
    for (alpha, gamma) in alphas_gammas:
        window = Window(alpha, gamma, radars)
        window.setup()
        window.start()
