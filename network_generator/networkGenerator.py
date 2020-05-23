# network_generator.py
import random
from xmlGenerator import *
from typing import List, Generator, Tuple
import matplotlib.pyplot as plt
import numpy as np
import mathParser
import threading
import time
import scipy.fftpack
import os

rand=random.random

def isFloat(x : str) -> bool:
    x = x[1:] if x[0] == "-" else x
    return x.replace(".", "", 1).isdigit()

class Param(object):
    """
    Takes a string that is the param and splits it into the different parts to make it easier to work with.\n  
    Means that later things won't just be referencing indexes in lists
    """
    def __init__(self, param : str) -> None:
        paramParts = param.replace(" ", "").split(":") # Strip white space and turn to a better list
        try:
            self.name = paramParts[0]
            self.type = paramParts[1]
            self.value = paramParts[2]
            self.propState = paramParts[3]
        except:
            raise Exception("Invalid parameter")

class OnResetInit(object):
    """
    Takes a string that is the equation for onReset or init and splits it into the different parts to make it easier to work with.\n  
    Means that later things won't just be referencing indexes in lists. Similar to Param class but with less fields.
    """
    def __init__(self, equ : str, init : bool = False) -> None:
        equParts = equ.replace(" ", "").split(":") # Strip white space and turn to a better list
        try:
            self.name = equParts[0]
            self.operator = equParts[1]
            if isFloat(equParts[2]):
                self.value = equParts[2]
            else:
                self.value = ""
                last = False
                for c in equParts[2]:
                    if last == False and c.isalpha():
                        self.value += "deviceProperties->" if not init else "deviceState->"
                    self.value += str(c)
                    last = c.isalpha()
        except:
            e = "Invalid reset type" if not init else "Invalid init type"
            raise Exception(e) 

class Neuron(object):
    """
    A simple neuron class.
    It contains the following parameters:
    * name - the name of the neuron
    * props - a list of parameters used in the equations (includes constant properties and variable states)
    * states - a list of parameters that are variable, subset of props
    * connections - an array of 1 or 0 stating the connection of a neuron to other neurons

    Initialise with Neuron(name, props, connections)
    """
    def __init__(self, name : str, params : List[str], refractory : int) -> None:
        self.name = name
        self.props = list(map(lambda param: Param(param), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x.propState == "s" or x.propState == "sr", self.props))
        self.refractory = refractory

class NeuronConnections(object):
    """
    A class containing the connections for neurons.
    It contains the following parameters:
    * name - the name of the neuron
    * connections - an array of 1 or 0 stating the connection of a neuron to other neurons

    Initialise with NeuronConnections(name, props, connections)
    """
    def __init__(self, name : str, connections : List[int]) -> None:
        self.name = name
        self.connections = connections

class Network(object):
    """
    A simple neural network class.
    It contains the following parameters:
    * name - the name of the network
    * threshold - the threshold equation for setting when a neuron fires
    * equations - the list of equations used by the network
    * neurons -  a tuple containing a generator for the neuron properties (Neuron class) and connections (NeuronConnections class)
    * onReset - a set of assignments that happen when the threshold is met (format: state variable : operator : network property)
    * init - what to initialise states too
    * maxt - the maximum number of time steps
    * graphType - the type of network: gals, clocked
    
    Initialise with Neuron(name, equations, threshold, neurons, onReset, maxt)
    
    Contains the following functions:
    * makeGraph - function called on initialisation to generate a graph
    * printGraph - saves the graph to 'name.xml'. Called by the user
    """
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : Tuple[Generator[Neuron, None, None], Generator[NeuronConnections, None, None]], onReset : List[str], init : List[str], maxt : int, graphType : str) -> None:
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.type = graphType
        self.onReset = list(map(lambda equ: OnResetInit(equ), onReset))
        self.initValues = list(map(lambda equ: OnResetInit(equ, True), init)) 
        self.filename = f"{self.name}.xml"
        self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold, self.onReset, self.initValues, self.type)

    def makeGraph(self, neurons : Tuple[Generator[Neuron, None, None], Generator[NeuronConnections, None, None]], name : str, maxt : int, equations : List[str], threshold : str, onReset : List[str], initValues : List[str], graphType : str) -> None:              
        """
        Make a network graph based on the contructors parameters
        """
        def printDevices() -> None:
            """
            Print the percentage of devices generated
            """
            while activateTimer1 == True:
                print(f"Generated {int(count / numNeurons * 100)}% of devices ({count}).")
                time.sleep(1)
        
        def printEdges(graphType="") -> None:
            """
            Print the percentage of edges generated
            """
            while activateTimer2 == True:
                if (activateTimer1 == False):
                    print(f"Generated {int(count / numNeurons * 100)}% of edges ({countEdges}).")
                time.sleep(1)

        # Timer stuff for printing percentage done each second
        t1 = threading.Timer(1, printDevices)
        t2 = threading.Timer(1, printEdges)
        t1.start()
        t2.start()
        activateTimer1 = False
        activateTimer2 = False
    
        # Split up neurons tuple
        neurons, neuronConnections, numNeurons = neurons
        baseNeuron = next(neurons)

        # Replace R with random number and evaluate
        for l in baseNeuron.props:
            r = rand()
            l.value = eval(l.value.replace("R", str(r)))

        # Generate XML code 
        properties = '\n\t\t'.join(list(map(lambda prop : f"\t\t\t<Scalar name=\"{prop.name}\" type=\"{prop.type}\" default=\"{prop.value}\"/>", baseNeuron.props)))
        states = '\n\t\t'.join(list(map(lambda state : f"\t\t\t<Scalar name=\"{state.name}\" type=\"{state.type}\"/>", baseNeuron.states)))
        inits = '\n\t\t'.join(list(map(lambda var : f"\t\t\tdeviceState->{var.name} = deviceProperties->{var.name}; // Set initial {var.name} value", baseNeuron.states))) + "\n"
        inits += '\n\t\t'.join(list(map(lambda var : f"\t\t\tdeviceState->{var.name} {var.operator} {var.value}; // Set initial {var.name} value", initValues)))
        assignments = '\n\t\t'.join(list(map(lambda var : f"\t\t\t\t{var.type} &{var.name} = deviceState->{var.name}; // Assign {var.name}", baseNeuron.states)))
        equations = '\n\t\t\t'.join(list(map(lambda equ : f"\t\t\t\t{equ};", equations))) 
        onReset = '\n\t\t'.join(list(map(lambda equ: f"\t\t\t\t\t{equ.name} {equ.operator} {equ.value};", onReset)))
        
        with open(self.filename, 'w') as f:
            countEdges = 0
            count = 0
            activateTimer2 = True
            activateTimer1 = True

            # Generate skeleton XML
            if graphType == "clocked":
                devices =  devicesGenClocked(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenClocked(name, devices, maxt)
            elif graphType == "gals":
                devices =  devicesGenGALS(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenGALS(name, devices, maxt)
            elif graphType == "gals_bi":
                devices =  devicesGenGALS(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenGALS(name, devices, maxt)
            elif graphType.replace(" ", "").split("=")[0] == "relaxed_gals":
                try: 
                    relaxationValue = int(graphType.replace(" ", "").split("=")[1])
                    devices =  devicesGenGALS(properties, states, inits, assignments, equations, threshold, onReset, relaxationValue)
                    graphStuff = graphGenGALS(name, devices, maxt)
                except:
                    raise Exception(f"{graphType} is an invalid relaxed graph type. {relaxationValue} is not a int, this value neds to be the number of fanin values to ignore.")
            elif graphType == "extreme":
                devices =  devicesGenExtreme(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenExtreme(name, devices, maxt)
            elif graphType == "none":
                devices =  devicesGenNone(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenNone(name, devices, maxt)
            elif graphType == "barrier":
                devices =  devicesGenBarrier(properties, states, inits, assignments, equations, threshold, onReset)
                graphStuff = graphGenBarrier(name, devices, maxt)
            else:
                raise Exception(f"{graphType} is an invalid graph type.")
            
            f.writelines(graphStuff)
            f.write("\n\t\t<DeviceInstances>\t\t")

            if graphType == "clocked":
                f.write(f"\n\t\t\t<DevI id=\"clock\" type=\"clock\"><P>\"neuronCount\":{numNeurons}</P></DevI>\n")

            print("Generating devices.")

            propsfortest = [] # for test_model.py

            for neuron in neurons:
                
                row = []

                # Replace R with random number and evaluate
                for l in neuron.props:
                    r = rand()
                    l.value = eval(l.value.replace("R", str(r)))

                    row.append([l.name, l.value])
                
                propsfortest.append(row)
                
                neuronProps = ','.join(list(map(lambda prop : f"\"{prop.name}\":{prop.value}", neuron.props)))                
                device = f"\t\t\t<DevI id=\"{neuron.name}\" type=\"neuron\"><P>{neuronProps},\"refractory\":{neuron.refractory},\"seed\":{random.randint(0,4294967295)}</P></DevI>\n"
                f.write(device)
                count += 1     

            # stuff for test_model.py
            propsfortest = list(zip(*propsfortest))
            propsfortest = list(map(lambda x: (x[0][0], np.array(list(map(lambda y: y[1], x)))), propsfortest))

            f.write("\t\t</DeviceInstances>\n\t\t<EdgeInstances>\n")

            if graphType == "clocked":
                for i in range(numNeurons):
                    f.write(f"\t\t\t<EdgeI path=\"n_{i}:tick-clock:tick\" />\n\t\t\t<EdgeI path=\"clock:tock-n_{i}:tock\" />\n")
            
            count = 0
            countEdges = 0
            activateTimer1 = False

            print("Generated all devices.")
            print("Generating edges.")

            # For test_model.py
            edges = []

            connectionsTracker = {} # used for bidirectional gals
            for neuron in neuronConnections:
                row = [] # for test_model.py
                connections = []
                for idx, connection in enumerate(neuron.connections): 
                    countEdges += 1
                    if connection == 1: 
                        #weight = -rand() if rand() > 0.8 else 0.5 * rand() # TODO: change to better random values
                        weight = -rand() if idx > 0.8 * numNeurons else 0.5 * rand() # TODO: change to not be hardcoded to izhekevich 80/20 split
                        edge = f"\t\t\t<EdgeI path=\"{neuron.name}:input-n_{idx}:fire\"><P>\"weight\":{weight}</P></EdgeI>\n"
                        connections.append(edge)

                        row.append(weight)

                        if graphType == "gals_bi": # Once I have got a better way to avoid duplicate connections, remove this
                            connectionsTracker[(f"{neuron.name}", f"n_{idx}")] = 1
                    else:
                        row.append(0)
                edges.append(row)
                count += 1
                f.write("".join(connections))

            activateTimer2 = False

            # change this so it doesn't use the dict
            if graphType == "gals_bi":
                print("Generating reverse edges.")
                connections = []
                for c in connectionsTracker:
                    if (c[1], c[0]) not in connectionsTracker:
                        edge = f"\t\t\t<EdgeI path=\"{c[1]}:input-{c[0]}:fire\"><P>\"weight\":0.0</P></EdgeI>\n"
                        connections.append(edge)
                    countEdges += 1
                f.write("".join(connections))
                
            print("Generated all edges.")
            print("Running test.")
            ################################################################

            # test_model.py stuff
            propsfortest.append(('edges', np.array([np.array(xi) for xi in edges])))
            a = np.array(propsfortest[0][1], np.float32)
            b = np.array(propsfortest[1][1], np.float32)
            c = np.array(propsfortest[2][1], np.float32)
            d = np.array(propsfortest[3][1], np.float32)

            S = np.array(propsfortest[-1][1].transpose(), np.float32)

            swapNeurons, swapWeights = True, True
            fname = 'dataXXX2.npy'

            np.random.seed(123)
            random.seed(123)

            swaps = [i for i in range(numNeurons)]

            if swapNeurons or swapWeights:
                src, dst = random.randint(0, numNeurons-1), random.randint(0, numNeurons-1)
                permutations = 1
                swapsDone = []
                for i in range(permutations):
                    if swapNeurons:
                        if (len(swapsDone) >= numNeurons):
                            break
                        src, dst = random.randint(0, numNeurons-1), random.randint(0, numNeurons-1)
                        while src in swapsDone or dst in swapsDone:
                            src, dst = random.randint(0, numNeurons-1), random.randint(0, numNeurons-1)
                    if swapWeights:
                        S[:,[src, dst]] = S[:,[dst, src]] # swap column
                        S[[src, dst]] = S[[dst, src]] # swap row

                    print(src, "->", dst)
                    print(dst, "->", src)

                    a[src], a[dst] = a[dst], a[src]
                    b[src], b[dst] = b[dst], b[src]
                    c[src], c[dst] = c[dst], c[src]
                    d[src], d[dst] = d[dst], d[src]
                    
                    swaps[src], swaps[dst] = swaps[dst], swaps[src]
                    swapsDone.append(src)
                    swapsDone.append(dst)

            np.save('swaps.npy', np.array(swaps))

            Ne = 80
            Ni = 20
            epochs = 1000
            #re = np.random.uniform(0, 1, Ne)

            v = -65 * np.ones(Ne + Ni)
            u = b * v

            firings = []

            # print("a", a)
            # print("b", b)
            # print("c", c)
            # print("d", d)
            """
            print("s", end='')
            for r in S:
                print(r)
            #"""
            numFires = 0

            for t in range(epochs):
                I = np.concatenate([5 * np.random.normal(0, 1, Ne), 2 * np.random.normal(0, 1, Ni)])
                #I = np.concatenate([5 * np.full(Ne, 0.0), 2 * np.full(Ni, 0.0)])
                
                fired = np.argwhere(v >= 30).flatten()
                
                firings.append(list(fired))
                numFires += len(fired)

                v[fired] = c[fired]
                u[fired] = u[fired] + d[fired]

                #print(fired, u[fired])


                """
                if (len(fired) > 1):
                    print("indexes", fired)
                    print("values", S[fired])
                    print("sum", np.sum(S[fired],axis=0))
                #"""


                I += np.sum(S[fired],axis=0)

                v = v + 1 * (0.04 * v * v + 5 * v + 140 - u + I)  # step 0.5 ms
                #v = v + 0.5 * (0.04 * v * v + 5 * v + 140 - u + I)  # for numerical

                u = u + a * (b * v - u)                                    # stability

            print("Test resulted in", numFires, "fires.")
            np.save(fname, firings, allow_pickle=True)

            fig, axis = plt.subplots(1, 1)
            fig.suptitle("Plot of which neurons are firing at each epoch")
            
            axis.plot(range(epochs), list(map(lambda l: len(l), firings)))
            axis.set_xlim(0, epochs)
            axis.set_ylim(0, Ne+Ni)

            axis.set_xlabel("Epoch")
            axis.set_ylabel("Number of firing neurons")
            axis.set_title("Quantity of neurons firing")

            #plt.show()

            fig, axis = plt.subplots(1, 1)

            firings = list(zip(range(epochs), firings))
            firings = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings))
            firings = list(filter(lambda l: l != [], firings))
            firings = [j for i in firings for j in i]

            ydata, xdata = zip(*firings)

            axis.scatter(xdata, ydata, s=1)
            axis.set_xlim(0, epochs)
            axis.set_ylim(0, Ne+Ni)

            axis.set_xlabel("Epoch")
            axis.set_ylabel("Neuron")
            axis.set_title("When each neuron fires")

            #plt.show()

            print(f"Test results saved to {fname}")

            ################################################################

            
            f.write("\t\t</EdgeInstances>\n\t</GraphInstance>\n</Graphs>")

            activateTimer2 = False
        
        # Make sure to stop timers
        t1.cancel()
        t2.cancel()

    def printGraph(self) -> None:
        """
        Print the current Network type to a file
        """
        with open(self.filename, 'r') as f:
            print(f.read())
