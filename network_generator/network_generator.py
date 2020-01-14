# network_generator.py
import random
from horrible_string_stuff import *
from typing import List

rand=random.random

class Neuron(object):
    def __init__(self, name : str, params : List[str], connections : List[int]):
        self.name = name
        self.props = list(map(lambda el: el.replace(" ", "").split(":"), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x[3] == "s", list(map(lambda el: el.replace(" ", "").split(":"), params))))
        self.connections = connections

class Network(object):
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : List[Neuron], maxt):
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.graph = self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold)
   
    def makeGraph(self, neurons : List[str], name : str, maxt : int, equations : List[str], threshold : str) -> str:              
        deviceInstances = []
        edgeInstances = []
        
        properties = '\n\t\t'.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\" default=\"%s\"/>" % (el[0], el[1], el[2]), neurons[0].props)))
        states = '\n\t\t'.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\"/>" % (el[0], el[1]), neurons[0].states)))
        inits = '\n\t\t'.join(list(map(lambda el : "\t\t\tdeviceState->%s = deviceProperties->%s; // Set initial %s value" % (el[0], el[0], el[0]), neurons[0].states)))
        assignments = '\n\t\t'.join(list(map(lambda el : "\t\t\t\t%s &%s = deviceState->%s; // Assign %s" % (el[1], el[0], el[0], el[0]), neurons[0].states)))
        equations = '\n\t\t'.join(list(map(lambda el : "\t\t\t\t%s;" % el, equations))) 

        for neuron in neurons:
            neuronProps = ','.join(list(map(lambda el : "\"%s\":%s" % (el[0], el[2]), neuron.props)))
            device = "\t\t\t<DevI id=\"%s\" type=\"neuron\"><P>%s</P></DevI>\n" % (neuron.name, neuronProps)
            deviceInstances.append(device)
            connections = []
            for connection in range(len(neuron.connections)): 
                if neuron.connections[connection] == 1: 
                    weight = -rand() if rand() > 0.8 else 0.5 * rand() # change to random value
                    edge = "\t\t\t<EdgeI path=\"%s:input-%s:fire\"><P>\"weight\":%s</P></EdgeI>\n" % (neuron.name, neurons[connection].name, weight)
                    connections.append(edge)
            edgeInstances.append("".join(connections))
        
        devices =  devicesGen(properties, states, inits, assignments, equations, threshold)
        graph = graphGen(name, devices, maxt, deviceInstances, edgeInstances)

        return graph

    def saveGraph(self):
        filename = "%s.xml" % self.name
        file = open(filename, "w") 
        file.writelines(self.graph) 
        file.close()
        print(self.graph)
        print("Graph saved as:", filename)