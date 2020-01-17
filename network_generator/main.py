# main.py
from networkGenerator import *
from neuronListGenerator import genNeuronList
from random import randint

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

############
# Option 1 #
############

neurons = []

Ne=80
Ni=20
K=20

N=Ne+Ni
K=min(N,K)

for i in range(N):
    name = f"n_{i}"
    r = rand()
    params2 = [
        "a : float : 0.02 : s",
        "b : float : 0.2 : s",
        f"v : float : {-65+15*r*r} : s",
        f"u : float : {8-6*r*r} : s",
        f"fanin : uint32_t : {K} : p"
    ] 
    params1 = [
        f"a : float : {0.02+0.08*r} : s",
        f"b : float : {0.25-0.05*r} : s",
        "v : float : -65 : s",
        "u : float : 2 : s",
        f"fanin : uint32_t : {K} : p"
    ]
    connections = [0 for k in range(N)]
    for j in range(Ni):
        while True:
            p = randint(0, len(connections) - 1)
            if connections[p] == 0 and p != j:
                connections[p] = 1
                break
            
    params = params1 if i < Ni else params2
    neuron = Neuron(name, params, connections)
    neurons.append(neuron)

############
# Option 2 #
############

params = [
    ([
        "a : float : 0.02 : s",
        "b : float : 0.2 : s",
        "v : float : -56.968 : s",
        "u : float : 4.7875 : s",
        "fanin : uint32_t : 20 : p"
    ], 0.8),
    ([
        "a : float : 0.0785 : s",
        "b : float : 0.2134 : s",
        "v : float : -65 : s",
        "u : float : 2 : s",
        "fanin : uint32_t : 20 : p"
    ], 0.2)
]

neurons1 = genNeuronList(100, params, 0.2) # No random things like the other version :(

network = Network("test_gals", equations, "v >= 30", neurons, onReset, 10)
network.saveGraph()
