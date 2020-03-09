# main.py
from networkGenerator import Network, Neuron, rand
from neuronListGenerator import genNeurons
from random import randint
import sys

if __name__ == "__main__":

    network_name = sys.argv[1]

    # Differential equations
    equations = [
        "v = 0.5 * (0.04 * v * v + 5 * v + 140 - u + I)",
        "u = a * (b * v - u)"
    ]

    # On reset uses the properties values
    onReset = [
        "v : = : v", # param : what to do to param : property
        "u : += : u"
    ]

    Ne=80
    Ni=20
    K=20

    N=Ne+Ni
    K=min(N,K)

    r = rand()

    params = [
        ([
            "a : float : 0.02 : s",
            "b : float : 0.2 : s",
            f"v : float : {-65+15} : sr",
            f"u : float : {8-6} : sr",
            f"fanin : uint32_t : {K} : p"
        ], 0.8),
        ([
            f"a : float : {0.02+0.08} : sr",
            f"b : float : {0.25-0.05} : sr",
            "v : float : -65 : s",
            "u : float : 2 : s",
            f"fanin : uint32_t : {K} : p"
        ], 0.2)
    ]

    neurons = genNeurons(100, params, 0.2) # No random things like the other version :(

    network = Network(network_name, equations, "v = 0.5", neurons, onReset, 10)
    network.printGraph()


