# network_generator.py
import random
from xmlGenerator import *
from typing import List
from enum import Enum

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
    def __init__(self, name : str, params : List[str], connections : List[int]) -> None:
        self.name = name
        self.props = list(map(lambda param: Param(param), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x.propState == "s", self.props))
        self.connections = connections

class Network(object):
    """
    A simple neural network class.
    It contains the following parameters:
    * name - the name of the network
    * threshold - the threshold equation for setting when a neuron fires
    * equations - the list of equations used by the network
    * neurons -  a list of neurons (using Neuron class)
    * onReset - a set of assignments that happen when the threshold is met (format: state variable : operator : network property)
    * maxt - the maximum number of time steps
    
    Initialise with Neuron(name, equations, threshold, neurons, onReset, maxt)
    
    Contains the following functions:
    * makeGraph - function called on initialisation to generate a graph
    * saveGraph - saves the graph to 'name.xml'. Called by the user
    """
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : List[Neuron], onReset : List[str], maxt : int) -> None:
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.onReset = list(map(lambda equ: OnReset(equ), onReset))
        self.graph = self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold, self.onReset)
   
    def makeGraph(self, neurons : List[str], name : str, maxt : int, equations : List[str], threshold : str, onReset : List[str]) -> str:              
        """
        Make a newwork graph based on the contructors parameters
        """
        deviceInstances = []
        edgeInstances = []
        
        properties = '\n\t\t'.join(list(map(lambda prop : f"\t\t\t<Scalar name=\"{prop.name}\" type=\"{prop.type}\" default=\"{prop.value}\"/>", neurons[0].props)))
        states = '\n\t\t'.join(list(map(lambda state : f"\t\t\t<Scalar name=\"{state.name}\" type=\"{state.type}\"/>", neurons[0].states)))
        inits = '\n\t\t'.join(list(map(lambda var : f"\t\t\tdeviceState->{var.name} = deviceProperties->{var.name}; // Set initial {var.name} value", neurons[0].states)))
        assignments = '\n\t\t'.join(list(map(lambda var : f"\t\t\t\t{var.type} &{var.name} = deviceState->{var.name}; // Assign {var.name}", neurons[0].states)))
        equations = '\n\t\t'.join(list(map(lambda equ : f"\t\t\t\t{equ};", equations))) 
        onReset = '\n\t\t'.join(list(map(lambda equ: f"\t\t\t\t\t{equ.name} {equ.operator} deviceProperties->{equ.value};", onReset)))

        for neuron in neurons:
            neuronProps = ','.join(list(map(lambda prop : f"\"{prop.name}\":{prop.value}", neuron.props)))
            device = f"\t\t\t<DevI id=\"{neuron.name}\" type=\"neuron\"><P>{neuronProps}</P></DevI>\n"
            deviceInstances.append(device)
            connections = []
            for connection in range(len(neuron.connections)): 
                if neuron.connections[connection] == 1: 
                    weight = -rand() if rand() > 0.8 else 0.5 * rand() # change to better random values
                    edge = f"\t\t\t<EdgeI path=\"{neuron.name}:input-{neurons[connection].name}:fire\"><P>\"weight\":{weight}</P></EdgeI>\n"
                    connections.append(edge)
            edgeInstances.append("".join(connections))
        
        devices =  devicesGen(properties, states, inits, assignments, equations, threshold, onReset)
        graph = graphGen(name, devices, maxt, deviceInstances, edgeInstances)

        return graph

    def saveGraph(self) -> None:
        """
        Save the current Network type to a file
        """
        filename = f"{self.name}.xml"
        file = open(filename, "w") 
        file.writelines(self.graph) 
        file.close()
        print(self.graph)
        print("Graph saved as:", filename)
