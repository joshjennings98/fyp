from brian2 import *
G = PoissonGroup(100, rates=50*Hz)
M = SpikeMonitor(G)
run(100*ms)

plot(M.t/ms, M.i, '.k')
title("Example Spiking Neural Network")
xlabel('Time (ms)')
ylabel('Neuron index')
show()