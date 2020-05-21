# network_compare.py

import matplotlib.pyplot as plt
import numpy as np

numEpochs = 1000
numNeurons = 100
quantity = False

fig, axis = plt.subplots(1, 1)
fig.suptitle("Plot of the number of neurons that fire at each epoch")


axis.set_xlabel("Epoch")
axis.set_ylabel("Neuron")

firings1 = np.load('dataXXX1.npy', allow_pickle=True)
firings2 = np.load('dataXXX2.npy', allow_pickle=True)
swaps = list(np.load('swaps.npy', allow_pickle=True))

fTemp = np.copy(firings2)

allRows = []
for i, fires in enumerate(firings2):
    row = []
    for j, fire in enumerate(fires):
        row.append(swaps.index(fire))
    allRows.append(row)

if (quantity):
    # dataset 1 fix
    firings1 = list(map(lambda l: len(l), firings1))
    axis.plot(range(numEpochs), firings1)
   
    # dataset 2 fix
    firings2 = list(map(lambda l: len(l), firings2))
    axis.plot(range(numEpochs), firings2)

    axis.set_xlim(0, numEpochs)
    axis.set_ylim(0, max(firings1))
else:
    # dataset 1 fix
    firings1 = list(zip(range(numEpochs), firings1))
    firings1 = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings1))
    firings1 = list(filter(lambda l: l != [], firings1))
    firings1 = [j for i in firings1 for j in i]

    ydata, xdata = zip(*firings1)
    axis.scatter(xdata, ydata, s=1)

    # dataset 2 fix
    firings2 = list(zip(range(numEpochs), allRows))
    firings2 = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings2))
    firings2 = list(filter(lambda l: l != [], firings2))
    firings2 = [j for i in firings2 for j in i]
    
    ydata, xdata = zip(*firings2)
    axis.scatter(xdata, ydata, s=1)

    axis.set_xlim(0, numEpochs)
    axis.set_ylim(0, numNeurons)


plt.show()