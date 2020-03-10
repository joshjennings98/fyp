# neuronGenerator.py
from networkGenerator import Neuron, NeuronConnections
from random import randint, random
from typing import Tuple, List, Generator

def genNeuronProperties(num : int, params : List[Tuple[List[str], float, float, float]]) -> Generator[Neuron, None, None]:
    """
    A function for generating a list of neurons.
    * num - number of neurons to create
    * params - the list tuples of (params for the neurons, fraction of neurons with this set of params) <- should add up to 1.0
    * connectionProb - a rough probability for how many neurons each neuron is connected to
    """
    # yield first neuron twice since it's properties are used for initialisation
    yield Neuron("n_0", params[0][0], params[0][2])
    i = 0
    for param in params:
        refractoryPeriod = param[2]
        numOfThisNeuron = param[1]
        neuronLogic = param[0]

        for _ in range(int(num * numOfThisNeuron)):
            name = f"n_{i}" 
            neuron = Neuron(name, neuronLogic, refractoryPeriod)
            yield neuron
            i += 1 

def genConnections(num : int, params : List[Tuple[List[str], float, float, float]]) -> Generator[NeuronConnections, None, None]:
    i = 0
    for param in params:
        connectionProb = param[3]
        numOfThisNeuron = param[1]

        for _ in range(int(num * numOfThisNeuron)):
            name = f"n_{i}"
            if connectionProb != 1:
                connections = [0 for k in range(num)]
                for _ in range(int(connectionProb * num)):
                    while True:
                        p = randint(0, len(connections) - 1)
                        if connections[p] == 0 and p != i:
                            connections[p] = 1
                            break
            else:
                connections = [1 for k in range(num)]
                    
            neuron = NeuronConnections(name, connections)
            yield neuron
            i += 1 

def genNeurons(num : int, params : List[Tuple[List[str], float, float, float]]) -> Tuple[Generator[NeuronConnections, None, None], Generator[Neuron, None, None], int]:
    neurons = genNeuronProperties(num, params)
    connections = genConnections(num, params)
    return neurons, connections, num