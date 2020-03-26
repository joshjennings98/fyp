# visualisation.py

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

def plotLogFile(filename : str, type : str, numEpochs = 6000, numNeurons = 1000, title : str = "title", handlerLogMessage : str = "FIRE!") -> None:
    
    if (type == "when"):
        
        with open(filename, 'r') as f:
            lines = f.readlines()

        xdata = []
        ydata = []

        for line in lines:
            words = line.split(" ")
            if words[0] == "Epoch":
                if handlerLogMessage in line:
                    idx = int(words[1][:-1])
                    if idx < numEpochs + 1:
                        n = ''.join(c for c in words[3] if c.isdigit())
                        if n != '':
                            ydata.append(int(n))
                            xdata.append(idx)
        
        fig, axis = plt.subplots(1, 1)
        fig.suptitle("Plot of which neurons are firing at each epoch")
        
        axis.scatter(xdata, ydata, s=1)
        axis.set_xlim(0, numEpochs)
        axis.set_ylim(0, numNeurons)
        axis.set_xlabel("Epoch")
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        plt.show()
    
    elif (type == "quantity"):
        
        with open(filename, 'r') as f:
            lines = f.readlines()

        xdata = range(numEpochs + 1)
        ydata = [0] * (numEpochs + 1)

        for line in lines:
            words = line.split(" ")
            if words[0] == "Epoch":
                if handlerLogMessage in line:
                    idx = int(words[1][:-1])
                    ydata[idx] += 1
        
        fig, axis = plt.subplots(1, 1)
        fig.suptitle("Plot of the number of neurons that fire at each epoch")
        
        axis.plot(xdata, ydata)
        axis.set_xlim(0, numEpochs)
        axis.set_ylim(0, numNeurons)
        axis.set_xlabel("Epoch")
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        plt.show()

    else:
        raise Exception("Invalid plotting type. Please specify either 'when' for a graph of which neuron fires each epoch, or 'quantity' to print the quantity of neurons firing per epoch.")

plotLogFile("log1.txt", "when", title="GraphSchema Clocked Izikevich")
plotLogFile("log2.txt", "when", title="My Clocked Izikevich")
plotLogFile("log1.txt", "quantity", title="GraphSchema Clocked Izikevich")
plotLogFile("log2.txt", "quantity", title="My Clocked Izikevich")