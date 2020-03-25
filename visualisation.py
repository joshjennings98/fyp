# visualisation.py

epochs = 6000
numNeurons = 1000

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
fig.suptitle("Plot of which neurons are firing at each epoch")
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


newx1 = {}
newx2 = {}
x3 = []
y3 = []
x4 = []
y4 = []

for x in x1:
    if x not in newx1:
        newx1[x] = (x, 1)
    else:
        newx1[x] = (x, newx1[x][1]+1)

for i in range(epochs):
    if i not in newx1:
        newx1[i] = (i, 0)

for x in x2:
    if x not in newx2:
        newx2[x] = (x, 1)
    else:
        newx2[x] = (x, newx2[x][1]+1)

for i in range(epochs):
    if i not in newx2:
        newx2[i] = (i, 0)

for value in sorted(newx1.values()):
    x3.append(value[0])
    y3.append(value[1])

for value in sorted(newx2.values()):
    x4.append(value[0])
    y4.append(value[1])


fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Plot of the number of neurons that fire at each epoch")
ax1.plot(x3, y3)
ax2.plot(x4, y4)

ax1.set_xlim(0, epochs)
ax1.set_ylim(0, numNeurons)
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Number of neurons firing")
ax1.set_title("Clocked Izikevich in Graph Schema repository")

ax2.set_xlim(0, epochs)
ax2.set_ylim(0, numNeurons)
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Number of neurons firing")
ax2.set_title("Clocked Izikevich generated using my code")

plt.show()