# main.py
from networkGenerator import Network, Neuron, rand
from neuronGenerator import genNeurons
from random import randint
import sys

if __name__ == "__main__":

    if len(sys.argv) > 1:
        network_name = sys.argv[1]
    else:
        network_name = "test_network"

    # Differential equations
    equations = [
        "v = 0.04 * v * v + 5 * v + 140 - u + I",
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
            f"v : float : {-65+15} : sr", # sr is state but the value will be multipled by a random number between 0 and 1
            f"u : float : {8-6} : sr",
            f"fanin : uint32_t : {K} : p"
        ], 0.8, 0, 0.2), # 2nd to last number is refractory period, last is connection probability
        ([
            f"a : float : {0.02+0.08} : sr",
            f"b : float : {0.25-0.05} : sr",
            "v : float : -65 : s",
            "u : float : 2 : s",
            f"fanin : uint32_t : {K} : p"
        ], 0.2, 0, 0.2)
    ]

    neurons = genNeurons(10000, params)

    network = Network(network_name, equations, "v >= 0.5", neurons, onReset, 10)
    # network.printGraph()


