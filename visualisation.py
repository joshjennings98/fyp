# visualisation.py

epochs = 3000
numNeurons = 100

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

def parseLogFile(filename : str) -> Tuple[List[int], List[int]]:
    lines = ""

    with open(filename, 'r') as f:
        lines = f.readlines()

    xdata = []
    ydata = []

    for line in lines:
        words = line.split(" ")
        if words[0] == "Epoch":
            if ',' in words[1] and "FIRE!" in line:
                idx = int(words[1][:-1])
                if idx < epochs + 1:
                    n = ''.join(c for c in words[3] if c.isdigit())
                    if n != '':
                        ydata.append(int(n))
                        xdata.append(idx)
    return xdata, ydata

x1, y1 = parseLogFile("log1.txt")
x2, y2 = parseLogFile("log2.txt")

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Plot of which neurons fire at which epoch")
ax1.scatter(x1, y1, s=1)
ax2.scatter(x2, y2, s=1)

ax1.set_xlim(0, epochs)
ax1.set_ylim(0, numNeurons)
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Neuron")
ax1.set_title("Clocked Izikevich in Graph Schema repository")

ax2.set_xlim(0, epochs)
ax2.set_ylim(0, numNeurons)
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Neuron")
ax2.set_title("Clocked Izikevich generated using my code")

plt.show()
    