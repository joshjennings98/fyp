# visualisation.py

import numpy as np
import matplotlib.pyplot as plt

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
            if handlerLogMessage in line:
                if ty == "epoch":
                    #if tx == "clocked":
                    idx = int(words[1][:-1])
                    if idx < numEpochs + 1:
                        n = ''.join(c for c in words[3] if c.isdigit())
                        if n != '':
                            ydata.append(int(n))
                            xdata.append(idx)
                    """
                    elif tx == "gals":
                        n = ''.join(c for c in words[3] if c.isdigit())
                        ydata.append(int(n)) 
                        xdata.append(words[-1])
                    """
                elif ty == "graph":
                    if tx == "clocked":
                        raise Exception("Clocked not yet supported")
                    elif tx == "gals":
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

        xdata = range(numEpochs + 1)
        ydata = [0] * (numEpochs + 1)

        for line in lines:
            words = line.split(" ")
            if handlerLogMessage in line:
                if ty == "epoch":
                    #if tx == "clocked":
                    idx = int(words[1][:-1])
                    if idx < numEpochs + 1:
                        ydata[idx] += 1
                    """
                    elif tx == "gals":
                        ydata[int(words[-1])] += 1
                    """
                elif ty == "graph":
                    if tx == "clocked":
                        raise Exception("Clocked not yet supported")
                    elif tx == "gals":
                        ydata[int(words[-1])] += 1
        
        fig, axis = plt.subplots(1, 1)
        fig.suptitle("Plot of the number of neurons that fire at each epoch")

        axis.plot(xdata, ydata)
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

    else:
        raise Exception("Invalid plotting type. Please specify either 'when' for a graph of which neuron fires each epoch, or 'quantity' to print the quantity of neurons firing per epoch.")

"""
plotLogFile("log_clocked_epoch.txt", "when", title="GraphSchema Clocked Izikevich (epoch_sim)", numEpochs = 3000, numNeurons = 1000, tx="clocked", ty="epoch")
plotLogFile("log_clocked_epoch.txt", "quantity", title="GraphSchema Clocked Izikevich (epoch_sim)", numEpochs = 3000, numNeurons = 1000, tx="clocked", ty="epoch")

plotLogFile("log_clocked_epoch_josh.txt", "when", title="My Clocked Izikevich (epoch_sim)", numEpochs = 3000, numNeurons = 1000, tx="clocked", ty="epoch")
plotLogFile("log_clocked_epoch_josh.txt", "quantity", title="My Clocked Izikevich (epoch_sim)", numEpochs = 3000, numNeurons = 1000, tx="clocked", ty="epoch")

plotLogFile("log_gals_epoch.txt", "when", title="GraphSchema GALS Izikevich (epoch_sim)", numEpochs = 1000, numNeurons = 100, tx="gals", ty="epoch")
plotLogFile("log_gals_epoch.txt", "quantity", title="GraphSchema GALS Izikevich (epoch_sim)", numEpochs = 1000, numNeurons = 100, tx="gals", ty="epoch")

plotLogFile("log_gals_epoch_josh.txt", "when", title="My GALS Izikevich (epoch_sim)", numEpochs = 1000, numNeurons = 1000, tx="gals", ty="epoch")
plotLogFile("log_gals_epoch_josh.txt", "quantity", title="My GALS Izikevich (epoch_sim)", numEpochs = 1000, numNeurons = 1000, tx="gals", ty="epoch")

plotLogFile("log_gals_graph.txt", "when", title="GraphSchema GALS Izikevich (graph_sim)", numEpochs = 1000, numNeurons = 100, tx="gals", ty="graph")
plotLogFile("log_gals_graph.txt", "quantity", title="GraphSchema GALS Izikevich (graph_sim)", numEpochs = 1000, numNeurons = 100, tx="gals", ty="graph")

plotLogFile("log_gals_graph_josh.txt", "when", title="My GALS Izikevich (graph_sim)", numEpochs = 1000, numNeurons = 1000, tx="gals", ty="graph")
plotLogFile("log_gals_graph_josh.txt", "quantity", title="My GALS Izikevich (graph_sim)", numEpochs = 1000, numNeurons = 1000, tx="gals", ty="graph")
"""

plotLogFile("log2.txt", "quantity", title="My Clocked Fully Connected (epoch_sim)", numEpochs = 100, numNeurons = 1000, tx="gals", ty="epoch")
plotLogFile("log2.txt", "when", title="My Clocked Fully Conencted (epoch_sim)", numEpochs = 100, numNeurons = 1000, tx="gals", ty="epoch")

