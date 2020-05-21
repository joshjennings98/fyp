from brian2 import *

seed(123)

start_scope()

Ne, Ni = 80, 20
duration = 1000 * ms

# General equations for Izhikevich neurons
eqs = '''
dv/dt = (0.04 / ms / mV) * v ** 2 + (5 / ms) * v + 140 * mV / ms - u + I : volt
du/dt = a * (b * v - u)                               			 : volt/second
a                                           		     	         : 1/second
b                                              				 : 1/second
c                                          			         : volt
d                                            	  			 : volt/second
'''

# Reset is the same for all neurons
reset = '''
v = c
u = u + d
'''

# Create excitatory and inhibitory thalamic inputs
I_Ne = '''
I = 5 * rand() * mV / ms						 : volt/second (constant over dt)
'''

# Inhibitory neurons thalamic input
I_Ni = '''
I = 2 * rand() * mV / ms						 : volt/second (constant over dt)
'''

# Excitatory neurons setup
G_Ne = NeuronGroup(Ne, eqs + I_Ne, threshold = 'v >= 30 * mV', reset=reset, method='euler') 

G_Ne.a = 0.02 / ms
G_Ne.b = 0.2 / ms
G_Ne.c = (-65 + 15 * rand() ** 2) * mV
G_Ne.d = (8 - 6 * rand() ** 2) * mV / ms
G_Ne.v = -G_Ne.c
G_Ne.u = G_Ne.b * G_Ne.c
G_Ne.I = 5 * rand() * mV / ms	

# Inhibitory neurons setup
G_Ni = NeuronGroup(Ni, eqs + I_Ni, threshold = 'v >= 30 * mV', reset=reset, method='euler') 

G_Ni.a = (0.02 + 0.08 * rand()) / ms
G_Ni.b = (0.25 - 0.05 * rand()) / ms
G_Ni.c = -65 * mV
G_Ni.d = 2 * mV / ms
G_Ni.v = G_Ni.c
G_Ni.u = G_Ni.b * G_Ni.c
G_Ni.I = 2 * rand() * mV / ms

# Create synapses
S1 = Synapses(G_Ne, G_Ne, 'w : volt/second', on_pre='I += w') # excitatory and excitatory
S2 = Synapses(G_Ne, G_Ni, 'w : volt/second', on_pre='I += w') # excitatory and inhibitory
S3 = Synapses(G_Ni, G_Ni, 'w : volt/second', on_pre='I += w') # inhibitory and inhibitory
S4 = Synapses(G_Ni, G_Ne, 'w : volt/second', on_pre='I += w') # inhibitory and excitatory

for S in [S1, S2, S3, S4]:
    S.connect(p=1.0)
    
    if S in [S1, S2]:
        S.w = 0.5 * rand() * mV / ms
    else:
        S.w = -rand() * mV / ms

# Simulate and plot
M_Ne = SpikeMonitor(G_Ne)
M_Ni = SpikeMonitor(G_Ni)

run(duration)

figure
plot(M_Ne.t/ms, M_Ne.i, '.k')
plot(M_Ni.t/ms, M_Ni.i + Ne, '.k') # Offset of Ne on y axis so it doesn't overlay on top of Ni neurons
xlabel('Time (ms)')
ylabel('Neuron index')
show()
