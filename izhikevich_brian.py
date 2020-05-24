import time
from brian2 import *

seed(123)

start_scope()

# Set up external parameters
duration = 100 * ms
Ne, Ni = 80, 20
density = 1.0

print(f"Izhikevich Network:\n- Ne = {Ne}\n- Ni = {Ni}\n- Density = {density}\n- Duration = {duration / ms} ms", end='\n\n')

# Set up with neuron indexes to monitor (optional)
monitorIndexes = []

# Izhikevich neuron equations
eqs = '''
dv/dt = (0.04 / ms / mV) * v ** 2 + (5 / ms) * v + 140 * mV / ms - u + I : volt
du/dt = a * (b * v - u) : volt/second
a : 1/second
b : 1/second
c : volt
d : volt/second
I : volt/second
'''

# Reset is the same for all neurons
reset = '''
v = c
u = u + d
'''

print("Generating Neurons", end=' ')

t1 = time.perf_counter()

# Neuron groups
G = NeuronGroup(Ne+Ni, eqs, threshold = 'v >= 30 * mV', reset=reset, method='euler') 
Ge = G[:Ne] # Excitatory
Gi = G[Ne:] # Inhibitory

# Excitatory specific parameters
Ge.a = 0.02 / ms
Ge.b = 0.2 / ms
Ge.c = [(-65 + 15 * rand() ** 2) * mV for _ in range(Ne)]
Ge.d = [(8 - 6 * rand() ** 2) * mV / ms for _ in range(Ne)]

# Inhibitory specific parameters
Gi.a = [(0.02 + 0.08 * rand()) / ms for _ in range(Ni)]
Gi.b = [(0.25 - 0.05 * rand()) / ms for _ in range(Ni)]
Gi.c = -65 * mV
Gi.d = 2 * mV / ms

# Global neuron parameters
G.v = -65 * mV
G.u = G.b * G.v

# Send the thalamic input every time step (1ms)
@network_operation(dt=1*ms)
def thalamic_input():
    Ge.I = [5 * randn() * mV / ms for i in range(Ne)]
    Gi.I = [2 * randn() * mV / ms for i in range(Ni)]

print("\rNeurons generated.\nGenerating Synapses", end=' ')

# Create Synapses and connections
Se = Synapses(Ge, G, 'w : volt/second', on_pre='I += w')
Si = Synapses(Gi, Ge, 'w : volt/second', on_pre='I += w')

for S in [Se, Si]:
    S.connect(p=density)
    
    if S == Se:
        S.w = 0.5 * rand() * mV / ms
    else:
        S.w = -rand() * mV / ms

t2 = time.perf_counter()

print(f"\rSynapses generated.\nNetwork generation completed in {t2 - t1:0.5f} seconds.\n\nRunning Simulation ", end='')

# Simulate and plot
spikes = SpikeMonitor(G)

if monitorIndexes != []: # optionally monitor specific neurons
    potentials = StateMonitor(G, True, record=monitorIndexes) 
    
run(duration)

t3 = time.perf_counter()

print(f"\rNetwork simulation completed in {t3 - t2:0.5f} seconds.\nNumber of fires: {len(spikes.i)}\n")

figure(figsize=(20, 16), dpi=80)
scatter(spikes.t/ms, spikes.i, s=1)
title(f"Izhikevich Network Simulation (BRIAN)\n(Ne={Ne}, Ni={Ni}, Density={density})\nPlot of when neurons fire")
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0, duration / ms)
ylim(0, Ne + Ni)
show()

if monitorIndexes != []:
    figure(figsize=(20, 16), dpi=80)
    plot(potentials.t, potentials.v.T)
    title(f"Izhikevich Network Simulation (BRIAN)\n(Ne={Ne}, Ni={Ni}, Density={density})\nMembrane Potential of specific neurons")
    xlabel('Time (s)')
    ylabel('Membrane Potential (V)')
    legend(list(map(lambda i: f"Neuron {i}", monitorIndexes)))
    show()