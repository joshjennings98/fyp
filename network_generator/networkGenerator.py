# network_generator.py
import random
from xmlGenerator import *
from typing import List, Generator
from enum import Enum
import os
import shutil
import ctypes
import platform
import sys

def getFreeSpace():
    """
    Return folder/drive free space in bytes.
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('%CD%'), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs('/')
        return st.f_bavail * st.f_frsize

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
    def __init__(self, name : str, params : List[str], connections : List[int], refractory : int) -> None:
        self.name = name
        self.props = list(map(lambda param: Param(param), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x.propState == "s" or x.propState == "sr", self.props))
        self.connections = connections
        self.refractory = refractory

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
    * printGraph - saves the graph to 'name.xml'. Called by the user
    """
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : Generator[Neuron, None, None], onReset : List[str], maxt : int) -> None:
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.onReset = list(map(lambda equ: OnReset(equ), onReset))
        self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold, self.onReset)
   
    def makeGraph(self, neurons : Generator[Neuron, None, None], name : str, maxt : int, equations : List[str], threshold : str, onReset : List[str]) -> None:              
        """
        Make a network graph based on the contructors parameters
        """
        baseNeuron = next(neurons)
        
        properties = '\n\t\t'.join(list(map(lambda prop : f"\t\t\t<Scalar name=\"{prop.name}\" type=\"{prop.type}\" default=\"{prop.value}\"/>", baseNeuron.props)))
        states = '\n\t\t'.join(list(map(lambda state : f"\t\t\t<Scalar name=\"{state.name}\" type=\"{state.type}\"/>", baseNeuron.states)))
        inits = '\n\t\t'.join(list(map(lambda var : f"\t\t\tdeviceState->{var.name} = deviceProperties->{var.name}; // Set initial {var.name} value", baseNeuron.states)))
        assignments = '\n\t\t'.join(list(map(lambda var : f"\t\t\t\t{var.type} &{var.name} = deviceState->{var.name}; // Assign {var.name}", baseNeuron.states)))
        equations = '\n\t\t\t'.join(list(map(lambda equ : f"\t\t\t\t{equ};", equations))) 
        onReset = '\n\t\t'.join(list(map(lambda equ: f"\t\t\t\t\t{equ.name} {equ.operator} deviceProperties->{equ.value};", onReset)))
        
        filename0 = f"{self.name}.xml"
        filename1 = f"{self.name}1.xml"
        filename2 = f"{self.name}2.xml"

        with open(filename1, 'w') as f1, open (filename2, 'w') as f2:
            devices =  devicesGen(properties, states, inits, assignments, equations, threshold, onReset)
            graphStuff = graphGen(name, devices, maxt)
            f1.writelines(graphStuff)
            f1.write("\t\t<DeviceInstances>\t\t\n")
            f2.write("\t\t</DeviceInstances>\n\t\t<EdgeInstances>\n")

            count = 0 # Keep track of iteration

            for neuron in neurons:
                neuronProps = ','.join(list(map(lambda prop : f"\"{prop.name}\":{prop.value if (prop.propState != 'sr') else float(prop.value) * rand()}", neuron.props)))
                device = f"\t\t\t<DevI id=\"{neuron.name}\" type=\"neuron\"><P>{neuronProps},\"refractory\":{neuron.refractory}</P></DevI>\n"
                f1.write(device)
        
                connections = []
                for connection in range(len(neuron.connections)): 
                    if neuron.connections[connection] == 1: 
                        weight = -rand() if rand() > 0.8 else 0.5 * rand() # change to better random values
                        edge = f"\t\t\t<EdgeI path=\"{neuron.name}:input-n_{connection}:fire\"><P>\"weight\":{weight}</P></EdgeI>\n"
                        connections.append(edge)
                f2.write("".join(connections))

                count += 1
                if count % 200 == 0:
                    print(f"Generated {count} neurons.")
        
            f2.write("\t\t</EdgeInstances>\n\t</GraphInstance>\n</Graphs>")
            
        edgeFileSize = os.stat(filename2).st_size
        storageLeft = getFreeSpace()
        
        if (edgeFileSize < storageLeft):
            with open (filename1, 'a') as f1, open (filename2, 'r') as f2:
                print("Merging intermediate files.")
                f1.writelines(f2)
                os.rename(filename1, filename0)
                print("Deleting duplicate files.")
                os.remove(filename2)
                print("File", filename0, "generated.")    
        else:
            print("The system needs to merge intermediate files.\n")
            print("Python cannot efficiently remove the first line from a file whilst copying it to another file.")
            print("This unfortunately means that the contents of the edges file need to be duplicated.\n")
            print(f"Your edges file is {edgeFileSize} bytes, but you only have {storageLeft} bytes available.\n")
            print("Since you do not have enough storage for this operation it has been terminated.")
            print(f"The devices file and edges file have been saved as {filename1} and {filename2} respectively.")
            print("You can keep these files and merge them yourself or you can delete them.\n")
            x = "NULL"
            while (x not in "yYnN"):
                print(f"Would you like to delete {filename1} and {filename2}? (y/n)")
                x = input()
            if (x in "yY"):
                os.remove(filename1)
                os.remove(filename2)

    def printGraph(self) -> None:
        """
        Print the current Network type to a file
        """
        filename = f"{self.name}.xml"
        with open(filename, 'r') as f:
            print(f.read())
