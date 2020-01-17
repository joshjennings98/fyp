# neuronListGenerator.py
from networkGenerator import Neuron
from random import randint, random
from typing import Tuple, List

def genNeuronList(num : int, params : List[Tuple[List[str], float]], connectionProb : float) -> List[Neuron]:
    """
    A function for generating a list of neurons.
    * num - number of neurons to create
    * params - the list tuples of (params for the neurons, fraction of neurons with this set of params) <- should add up to 1.0
    * connectionProb - a rough probability for how many neurons each neuron is connected to
    """
    neurons = []
    i = 0
    for param in params:
        for j in range(int(num * param[1])):
            name = f"n_{i}"
            if connectionProb != 1:
                connections = [0 for k in range(num)]
                for j in range(int(connectionProb * num)):
                    while True:
                        p = randint(0, len(connections) - 1)
                        if connections[p] == 0 and p != j:
                            connections[p] = 1
                            break
            else:
                connections = [1 for k in range(num)]
                    
            neuron = Neuron(name, param[0], connections)
            neurons.append(neuron)
            i += 1
    
    return neurons

