# neuronGenerator.py
from networkGenerator import Neuron
from random import randint, random
from typing import Tuple, List, Generator

def genNeurons(num : int, params : List[Tuple[List[str], float, float]], connectionProb : float) -> Generator[Neuron, None, None]:
    """
    A function for generating a list of neurons.
    * num - number of neurons to create
    * params - the list tuples of (params for the neurons, fraction of neurons with this set of params) <- should add up to 1.0
    * connectionProb - a rough probability for how many neurons each neuron is connected to
    """
    # yield first neuron twice since it's properties are used
    yield Neuron("n_0", params[0][0], [0 for k in range(num)], params[0][2])
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
                    
            neuron = Neuron(name, param[0], connections, param[2])
            yield neuron
            i += 1 
