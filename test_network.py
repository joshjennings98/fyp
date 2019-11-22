# test_network.py

from test_generator import makeGraph, saveGraph, Neuron

name = "test_network"
maxt = 100

neurons = [
    Neuron("n_0", 1, [0, 1, 0, 0, 0]),
    Neuron("n_1", 0, [0, 0, 1, 0, 0]),
    Neuron("n_2", 0, [0, 0, 0, 1, 0]),
    Neuron("n_3", 0, [0, 0, 0, 0, 1]),
    Neuron("n_4", 0, [1, 0, 0, 0, 0]),
]

graph = makeGraph(neurons, name, maxt)

saveGraph(graph, "test_network.xml")