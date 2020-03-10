# nonConfigInitExample.py
#
# This version of the network doesn't use the config file.
# It shows how the network is viewed in the backend and shouldn't be deleted.
# This way you can do more complex stuff that isn't possible using the config file.

import sys
from networkGenerator import Network, Neuron, rand
from neuronGenerator import genNeurons

network_name = "test_network" # Don't change this if using test.sh

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

# The params for the neurons
params = [
    ([
        "a : float : 0.02 : s",
        "b : float : 0.2 : s",
        "v : float : -50 : sr", # sr is state but the value will be multipled by a random number between 0 and 1
        "u : float : 2 : sr",
        "fanin : uint32_t : 20 : p"
    ], 0.8, 0, 0.2), # 2nd to last number is refractory period, last is connection probability
    ([
        f"a : float : 0.1 : sr",
        f"b : float : 0.2 : sr",
        "v : float : -65 : s",
        "u : float : 2 : s",
        f"fanin : uint32_t : 20 : p"
    ], 0.2, 0, 0.2)
]

neurons = genNeurons(100, params) # neurons needs to be a generator of neurons and a generator of connections

# Generate and print network
network = Network(network_name, equations, "v >= 0.5", neurons, onReset, 10)
network.printGraph()
