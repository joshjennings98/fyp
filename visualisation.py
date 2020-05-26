# visualisation.py

import numpy as np
from scipy.spatial import distance
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
                elif tx == "clocked":
                    if handlerLogMessage in line:
                        xdata.append(int(''.join(c for c in words[1] if c.isdigit())) // 3) 
                        ydata.append(int(''.join(c for c in words[3] if c.isdigit())))
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
                        curClock = int(words[-2])  # or words[-1]
                    elif handlerLogMessage in line:
                        #ydata.append(int(''.join(c for c in words[0] if c.isdigit()))) 
                        ydata.append(int(''.join(c for c in words[4].replace('(0)=', '') if c.isdigit()))) 
                        xdata.append(curClock)
                        print(ydata[-1])
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

        testLen = len(xdata)
        oldy = []
        oldx = []

        for y in ydata:
            oldy.append(y)

        for x in xdata:
            oldx.append(x)

        print("Number of fires:", testLen)
        
        axis.scatter(xdata, ydata, s=1)
        axis.set_xlim(0, numEpochs // 3 + 1 if tx == "clocked" else numEpochs)
        axis.set_ylim(0, numNeurons)
        
        if ty == "epoch":
            epochOrTimestep = "Epoch"
        elif ty == "graph":
            epochOrTimestep = "Time Step"
        
        axis.set_xlabel(epochOrTimestep)
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        firings = np.load('data.npy', allow_pickle=True)
        
        firings = list(zip(range(numEpochs // 3 + 1 if tx == "clocked" else numEpochs), firings))
        firings = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings))
        firings = list(filter(lambda l: l != [], firings))
        firings = [j for i in firings for j in i]
        
        ydata, xdata = zip(*firings)
        axis.scatter(xdata, ydata, s=1, color='red')
        
        plt.show()

        y1 = [0 for _ in range(1 + (numEpochs // 3 + 1 if tx == "clocked" else numEpochs))]
        y2 = [0 for _ in range(1 + (numEpochs // 3 + 1 if tx == "clocked" else numEpochs))]
        newX = [i for i in range(1 + (numEpochs // 3 + 1 if tx == "clocked" else numEpochs))]

        for i in range(min(len(xdata), testLen)):
            #print(xdata[i], oldx[i])
            y1[xdata[i]] += 1
            y2[oldx[i]+1] += 1

        #for i in range(len(list(zip(y1, y2))) // 10):
        #    print(list(zip(y1, y2))[i])

        difference = [abs(a - b) for a, b in zip(y1, y2)]

        a = sorted(list(zip(xdata, ydata)))
        b = sorted(list(zip(oldx, oldy)))

        newA, newB = [], []
        newA1, newB1 = [], []
        for i in range(min(len(a), len(b))):
            if a[i][1] < 80:
                newA.append(a[i])
                newB.append(b[i])
            else:
                newA1.append(a[i])
                newB1.append(b[i])

        a, b = np.array(newA), np.array(newB)

        a1, b1 = np.array(newA1), np.array(newB1)

        ecl = []
        ecl1 = []
        
        for i in range(len(newA)):
            ecl.append(distance.euclidean(a[i], b[i]) - 1)

        for i in range(len(newA1)):
            ecl1.append(distance.euclidean(a1[i], b1[i]) - 1)
        
        #print(list(zip(xdata, ecl)))

        xd, yd = zip(*list(zip(list(map(lambda x : x[0], newA)), ecl)))
        xd1, yd1 = zip(*list(zip(list(map(lambda x : x[0], newA1)), ecl1)))
            
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.suptitle("Euclidean distance between fires for hardware vs numpy simulation")
        ax1.scatter(xd, yd, s=1)
        ax1.set_title("Excitatory Neurons")
        ax1.set_ylabel("Euclidean distance")
        ax1.set_xlabel("Timestep")
        ax2.scatter(xd1, yd1, s=1, c='orange')
        ax2.set_title("Inhibitory Neurons")
        ax2.set_ylabel("Euclidean distance")
        ax2.set_xlabel("Timestep")

        fig, ax = plt.subplots(1, 1)
        fig.suptitle("MAE between number of fires in each epoch for hardware vs numpy simulation")
        ax.plot([i for i in range(len(difference))], difference)
        ax.set_ylabel("Mean Absolute Error")
        ax.set_xlabel("Timestep")

        print(f"Excitatory neurons error: Mean = {np.mean(yd)}, Variance = {np.var(yd)}")
        print(f"Inhibitory neurons error: Mean = {np.mean(yd1)}, Variance = {np.var(yd1)}")

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
                            curClock = int(words[-2]) # or words[-1]
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
        axis.set_ylim(0, max(ydata))
        
        if ty == "epoch":
            epochOrTimestep = "Epoch"
        elif ty == "graph":
            epochOrTimestep = "Time Step"
        
        axis.set_xlabel(epochOrTimestep)
        axis.set_ylabel("Neuron")
        axis.set_title(title)

        firings = np.load('data.npy', allow_pickle=True)
        
        axis.plot(range(numEpochs // 3 if tx == "clocked" else numEpochs), list(map(lambda l: len(l), firings)))
        """
        plt.close()
        fig, axis = plt.subplots(1, 1)

        L = 1000
        Y = np.fft.fft(list(map(lambda x: len(x), firings)))
        P2 = abs(Y/L)
        P1 = P2[:L//2+1]
        P1[1:-2] = 2*P1[1:-2]
        
        axis.plot(range(len(P1)), P1)

        Y = np.fft.fft(ydata)
        P2 = abs(Y/L)
        P1 = P2[:L//2+1]
        P1[1:-2] = 2*P1[1:-2]
        
        axis.plot(range(len(P1)), P1)

        axis.set_ylabel("Magnitude")
        axis.set_xlabel("Frequency")
        axis.set_title("fft of test_model (blue) and POETS (orange)")
        """

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
