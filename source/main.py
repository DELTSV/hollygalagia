import sys

from source.ui.Window import Window, load

alpha = float(sys.argv[1])
gamma = float(sys.argv[2])
radars = []

for i in range(3, len(sys.argv)):
    tmp = sys.argv[i].split(",")
    radars.append((int(tmp[0]), int(tmp[1])))

history = load(alpha, gamma, radars)
if history is None:
    history = []

window = Window(history, alpha, gamma, radars)
window.setup()
window.run()
