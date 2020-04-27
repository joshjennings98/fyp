# network_generator.py
import random
from xmlGenerator import *
from typing import List, Generator, Tuple
import threading
import time
import os

rand=random.random

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

class OnReset(object):
    """
    Takes a string that is the equation for onReset and splits it into the different parts to make it easier to work with.\n  
    Means that later things won't just be referencing indexes in lists. SImilar to Param class but with less fields.
    """
    def __init__(self, equ : str) -> None:
        equParts = equ.replace(" ", "").split(":") # Strip white space and turn to a better list
        try:
            self.name = equParts[0]
            self.operator = equParts[1]
            self.value = equParts[2]
        except:
            raise Exception("Invalid reset type")

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
    * maxt - the maximum number of time steps
    * graphType - the type of network: gals, clocked
    
    Initialise with Neuron(name, equations, threshold, neurons, onReset, maxt)
    
    Contains the following functions:
    * makeGraph - function called on initialisation to generate a graph
    * printGraph - saves the graph to 'name.xml'. Called by the user
    """
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : Tuple[Generator[Neuron, None, None], Generator[NeuronConnections, None, None]], onReset : List[str], maxt : int, graphType : str) -> None:
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.type = graphType
        self.onReset = list(map(lambda equ: OnReset(equ), onReset))
        self.filename = f"{self.name}.xml"
        self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold, self.onReset, self.type)

    def makeGraph(self, neurons : Tuple[Generator[Neuron, None, None], Generator[NeuronConnections, None, None]], name : str, maxt : int, equations : List[str], threshold : str, onReset : List[str], graphType : str) -> None:              
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
        
        # Generate C code
        properties = '\n\t\t'.join(list(map(lambda prop : f"\t\t\t<Scalar name=\"{prop.name}\" type=\"{prop.type}\" default=\"{prop.value}\"/>", baseNeuron.props)))
        states = '\n\t\t'.join(list(map(lambda state : f"\t\t\t<Scalar name=\"{state.name}\" type=\"{state.type}\"/>", baseNeuron.states)))
        inits = '\n\t\t'.join(list(map(lambda var : f"\t\t\tdeviceState->{var.name} = deviceProperties->{var.name}; // Set initial {var.name} value", baseNeuron.states)))
        assignments = '\n\t\t'.join(list(map(lambda var : f"\t\t\t\t{var.type} &{var.name} = deviceState->{var.name}; // Assign {var.name}", baseNeuron.states)))
        equations = '\n\t\t\t'.join(list(map(lambda equ : f"\t\t\t\t{equ};", equations))) 
        onReset = '\n\t\t'.join(list(map(lambda equ: f"\t\t\t\t\t{equ.name} {equ.operator} deviceProperties->{equ.value};", onReset)))
        
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

            for neuron in neurons:
                neuronProps = ','.join(list(map(lambda prop : f"\"{prop.name}\":{prop.value if (prop.propState != 'sr') else round(float(prop.value) * 0.001 * random.randrange(800, 1000, 1), 3)}", neuron.props)))
                device = f"\t\t\t<DevI id=\"{neuron.name}\" type=\"neuron\"><P>{neuronProps},\"refractory\":{neuron.refractory},\"seed\":{random.randint(0,4294967295)}</P></DevI>\n"
                f.write(device)
                count += 1     

            f.write("\t\t</DeviceInstances>\n\t\t<EdgeInstances>\n")

            if graphType == "clocked":
                for i in range(numNeurons):
                    f.write(f"\t\t\t<EdgeI path=\"n_{i}:tick-clock:tick\" />\n\t\t\t<EdgeI path=\"clock:tock-n_{i}:tock\" />\n")
            
            count = 0
            countEdges = 0
            activateTimer1 = False

            print("Generated all devices.")
            print("Generating edges.")

            connectionsTracker = {}
            for neuron in neuronConnections:
                connections = []
                for idx, connection in enumerate(neuron.connections): 
                    countEdges += 1
                    if connection == 1: 
                        weight = -rand() if rand() > 0.8 else 0.5 * rand() # TODO: change to better random values
                        #weight = -rand() if idx > 8*numNeurons//10 else 0.5 * rand()
                        edge = f"\t\t\t<EdgeI path=\"{neuron.name}:input-n_{idx}:fire\"><P>\"weight\":{weight}</P></EdgeI>\n"
                        connections.append(edge)
                        connectionsTracker[(f"{neuron.name}", f"n_{idx}")] = 1
                count += 1
                f.write("".join(connections))

            activateTimer2 = False

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
