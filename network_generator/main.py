from network_generator import *
from random import randint

neurons1 = [ # Props are "name : type : value : <property p or state s>"
    Neuron("n_0", [
            f"u : float : {-65+15*rand()*rand()} : s", 
            f"v : float : {8-6*rand()*rand()} : s", 
            "a : float : 0.02 : s", 
            "b : float : 0.2 : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [1, 0, 1, 0, 0]),
    Neuron("n_1", [
            f"u : float : {-65+15*rand()*rand()} : s", 
            f"v : float : {8-6*rand()*rand()} : s",       
            "a : float : 0.02 : s", 
            "b : float : 0.2 : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 0, 0, 1, 1]),
    Neuron("n_2", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*rand()} : s", 
            f"b : float : {0.25-0.05*rand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 1, 0, 1, 0]),
    Neuron("n_3", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*rand()} : s", 
            f"b : float : {0.25-0.05*rand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [1, 0, 0, 0, 1]),
    Neuron("n_4", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*rand()} : s", 
            f"b : float : {0.25-0.05*rand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 0, 1, 1, 0]),
]
    
equations = [
    "v = 0.5 * (0.04 * v * v + 5 * v + 140 - u + I)",
    "u = a * (b * v - u)"
]

neurons = []

Ne=80
Ni=20
K=20

N=Ne+Ni
K=min(N,K)

connections = []

for i in range(N):
    name = f"n_{i}"
    r = rand()
    params2 = [
        "a : float : 0.02 : s",
        "b : float : 0.2 : s",
        f"v : float : {-65+15*r*r} : s",
        f"u : float : {8-6*r*r} : s",
        #"Ir : float : 1 : p",
        f"fanin : uint32_t : {K} : p"
    ] 
    params1 = [
        f"a : float : {0.02+0.08*r} : s",
        f"b : float : {0.25-0.05*r} : s",
        "v : float : -65 : s",
        "u : float : 2 : s",
        #"Ir : float : 1 : p",
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

Network("test_gals", equations, "v >= 30", neurons, 10).saveGraph()