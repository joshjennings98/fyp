import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# n = number of neurons (independent) vary
# r = firing rate [0:1] (independent) vary
# d = average degree (independent) vary
# T = total time steps (independent) const

# c = number of clusters (independent)

# m = number of messages (dependent)
# t = time for one time step actual (dependent)

# W = t_a T

# GALS => m = n * d * T, t = max (t_synapse + t_return)_0..n
# Clocked => m = n * (1 + 2 * n + d) * r * T, t = max (t_clock1 + max(t_tick_0..n) + max(t_synapse_0..n))
# Clustered => m = n * r * (1 + c + d) * T, max (t_torepeater + max (t_betweenfpga) + max (t_fromrepeater))
# Barrier => m = n * d * T * r, t = max(t_synapse_0..n) + k_barrier
# Relaxed GALS => m = n * d * T, t = max ((t_synapse + t_return)_0..(relaxation * n))
# Non synced Leaky Integrate and Fire => m = n * d * T * r, t = max (t_synapse_0..n)
# Extreme Relaxed Leaky Integrate and Fire => m = n * d * T * r, t = max (t_synapse_0..n)

def galsMessages(degree : float, time : int, neurons : int) -> int:
    return neurons * time * (neurons * degree)

def clockedMessages(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (1 + 2 * neurons + (neurons * degree)) * fireProb * time

def clusterMessages(degree : float, time : int, neurons : int, fireProb : float, clusterSize : int) -> int:
    return neurons * fireProb * (1 + clusterSize + (neurons * degree)) * time

def barrierMessages(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

def relaxedGalsMessages(degree : float, time : int, neurons : int) -> int:
    return neurons * time * (neurons * degree)

def nonSyncedLIAFMessages(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

def extremeRelaxedLIAFMessages(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

degree = 0.2
time = 10000
fireProb = 0.6
clusterNum = 1000

formatter0 = EngFormatter()

x = [i for i in range(1,4*10**5, 100)]
y1 = list(map(lambda el: galsMessages(degree, time, el), x))
y2 = list(map(lambda el: clockedMessages(degree, time, el, fireProb), x))
y3 = list(map(lambda el: clusterMessages(degree, time, el, fireProb, clusterNum), x))
y4 = list(map(lambda el: barrierMessages(degree, time, el, fireProb), x))
y5 = list(map(lambda el: relaxedGalsMessages(degree, time, el), x))
y6 = list(map(lambda el: nonSyncedLIAFMessages(degree, time, el, fireProb), x))
y7 = list(map(lambda el: extremeRelaxedLIAFMessages(degree, time, el, fireProb), x))

fig = plt.figure()
fig.suptitle("Message Count vs Neuron Count (Izhekevich)", fontsize=16)

ax2 = fig.add_subplot(122)
ax2.set_xlabel("Neuron Count")
ax2.xaxis.set_major_formatter(formatter0)
ax2.set_ylabel("Message Count")
ax2.yaxis.set_major_formatter(formatter0)
firstN = 200
ax2.plot(x[0:firstN], y3[0:firstN], label=f'Clustered ({clusterNum} clusters)')
ax2.plot(x[0:firstN], y6[0:firstN], label='Non Synchronised Leaky Integrate and Fire')
ax2.plot(x[0:firstN], y7[0:firstN], label='Extreme Relaxed Leaky Integrate and Fire')
ax2.plot(x[0:firstN], y4[0:firstN], ":" ,label='Barrier')
ax2.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for Leaky-Integrate-And-Fire and Barrier)")
plt.legend()

ax = fig.add_subplot(121)
ax.set_xlabel("Neuron Count")
ax.xaxis.set_major_formatter(formatter0)
ax.set_ylabel("Message Count")
ax.yaxis.set_major_formatter(formatter0)

ax.plot(x, y1, label='GALS')
ax.plot(x, y2, label='Clocked')
ax.plot(x, y3, label=f'Clustered ({clusterNum} clusters)')
ax.plot(x, y4, label='Barrier')
ax.plot(x, y5, label='Relaxed GALS')
ax.plot(x, y6, label='Non Synchronised Leaky Integrate and Fire')
ax.plot(x, y7, label='Extreme Relaxed Leaky Integrate and Fire')
ax.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for relaxed and normal GALS)")


plt.legend()

plt.show()