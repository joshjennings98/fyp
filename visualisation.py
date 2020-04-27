# visualisation.py

import numpy as np
import matplotlib.pyplot as plt
from os import sys

def plotLogFile(filename : str, type : str, numEpochs = 6000, numNeurons = 1000, title : str = "title", handlerLogMessage : str = "FIRE!", tx : str = "clocked", ty : str = "epoch") -> None:
    """
    A simple function for plotting the output of epochsim outputs.
    To generate the log file when running epochsim add ' 2> filename' to the end of the epochsim command.
    
    It contains the following parameters:
    * filename - the silename of the log file
    * type - specify either 'when' for a graph of which neuron fires each epoch, or 'quantity' to print the quantity of neurons firing per epoch.
    * numEpochs - the number of epochs that you want to plot from epochsim (default 6000)
    * numNeurons - the number of neurons that you want to plot from epochsim (default 1000)
    * title - the title of the plot (default 'title')
    * handlerLogMessage - the message in the log file that is used to plot a spiking event (default 'FIRE!')
    """
    if (type == "when"):
        
        with open(filename, 'r') as f:
            lines = f.readlines()

        xdata = []
        ydata = []

        for line in lines:
            words = line.split(" ") 
            if ty == "epoch":
                if tx == "barrier":
                    if handlerLogMessage in line:
                        ydata.append(int(''.join(c for c in words[2] if c.isdigit()))) 
                        xdata.append(int(words[-1]))
                elif handlerLogMessage in line:
                    idx = int(words[1][:-1])
                    if idx < numEpochs + 1:
                        n = ''.join(c for c in words[3] if c.isdigit())
                        if n != '':
                            ydata.append(int(n))
                            xdata.append(idx)
            elif ty == "graph":
                if tx == "clocked":
                    if "time" in line:
                        curClock = int(words[-1])
                    elif handlerLogMessage in line:
                        ydata.append(int(''.join(c for c in words[0] if c.isdigit()))) 
                        xdata.append(curClock)
                elif tx == "gals":
                    if handlerLogMessage in line:
                        ydata.append(int(''.join(c for c in words[0] if c.isdigit()))) 
                        xdata.append(int(words[-1]))
                elif tx == "barrier":
                    if handlerLogMessage in line:
                        ydata.append(int(''.join(c for c in words[0] if c.isdigit()))) 
                        xdata.append(int(words[-1]))
                
        fig, axis = plt.subplots(1, 1)
        fig.suptitle("Plot of which neurons are firing at each epoch")
        
        axis.scatter(xdata, ydata, s=1)
        axis.set_xlim(0, numEpochs)
        axis.set_ylim(0, numNeurons)
        
        if ty == "epoch":
            epochOrTimestep = "Epoch"
        elif ty == "graph":
            epochOrTimestep = "Time Step"
        
        axis.set_xlabel(epochOrTimestep)
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        plt.show()
    
    elif (type == "quantity"):
        
        with open(filename, 'r') as f:
            lines = f.readlines()

        if tx == "clocked":
            ydata = [0] * (numEpochs // 3 + 1)  if ty == "epoch" else [0] * (numEpochs + 1)
            xdata = range(numEpochs // 3 + 1) if ty == "epoch" else range(numEpochs + 1)
        else:
            ydata = [0] * (numEpochs + 1)  if ty == "epoch" else [0] * (numEpochs + 1)
            xdata = range(numEpochs + 1) if ty == "epoch" else range(numEpochs + 1)

        curClock = 0

        for line in lines:
            words = line.split(" ") 
            if handlerLogMessage in line:
                if ty == "epoch":
                    if tx == "barrier":
                        ydata[int(words[-1]) - 1] += 1
                    elif tx == "clocked":
                        idx = int(words[1][:-1]) // 3
                        if idx < numEpochs // 3 + 1:
                            ydata[idx] += 1
                    else:
                        idx = int(words[1][:-1])
                        if idx < numEpochs + 1:
                            ydata[idx] += 1
                elif ty == "graph":
                    if tx == "clocked":
                        if "time" in line:
                            curClock = int(words[-1])
                        elif handlerLogMessage in line:
                            ydata[curClock] += 1
                    elif tx == "gals":
                        ydata[int(words[-1])] += 1
                    elif tx == "barrier":
                        ydata[int(words[-1]) - 1] += 1
        
        fig, axis = plt.subplots(1, 1)
        fig.suptitle("Plot of the number of neurons that fire at each epoch")

        axis.plot(xdata, ydata)
        axis.set_xlim(0, numEpochs // 3 + 1 if tx == "clocked" else numEpochs)
        axis.set_ylim(0, numNeurons)
        
        if ty == "epoch":
            epochOrTimestep = "Epoch"
        elif ty == "graph":
            epochOrTimestep = "Time Step"
        
        axis.set_xlabel(epochOrTimestep)
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        plt.show()

    else:
        raise Exception("Invalid plotting type. Please specify either 'when' for a graph of which neuron fires each epoch, or 'quantity' to print the quantity of neurons firing per epoch.")

if __name__ == "__main__":  
    
    if len(sys.argv) < 7:

        print("This script requires: name, plot type, num epochs, num neurons, clock type, and sim type.")
    
    elif len(sys.argv) == 7:

        name = sys.argv[1] 
        plotType = sys.argv[2]
        numEpochs = int(sys.argv[3])
        numNeurons = int(sys.argv[4])
        clockType = sys.argv[5]
        simType = sys.argv[6]
        handlerLogMessage = "FIRE!"
        title1 = "When neurons fire" if plotType == "when" else "Quantity of neurons firing"
        title = f"{name} - {title1} ({clockType}, {simType}sim)"

    elif len(sys.argv) == 9:

        name = sys.argv[1] 
        plotType = sys.argv[2]
        numEpochs = int(sys.argv[3])
        numNeurons = int(sys.argv[4])
        clockType = sys.argv[5]
        simType = sys.argv[6]
        title = sys.argv[7] 
        handlerLogMessage = sys.argv[8]

    else:
        
        print("This mode is not recommended.\nIf you still want to use it you need to provide:", end= " ")
        print("name, plot type, num epochs, num neurons, clock type, sim type, title, and handler_log message.")

    plotLogFile(name, plotType, numEpochs, numNeurons, title, handlerLogMessage, clockType, simType)
