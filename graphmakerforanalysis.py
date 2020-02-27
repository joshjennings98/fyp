import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# n = number of neurons (independent) vary
# r = firing rate [0:1] (independent) vary
# d = average degree (independent) vary (DONE AS A PERCENTAGE OF THE TOTAL NETWORK NODES)
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

def galsMessagesFrac(degree : float, time : int, neurons : int) -> int:
    return neurons * time * (neurons * degree)

def clockedMessagesFrac(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (1 + 2 * neurons + (neurons * degree)) * fireProb * time

def clusterMessagesFrac(degree : float, time : int, neurons : int, fireProb : float, clusterSize : int) -> int:
    return neurons * fireProb * (1 + clusterSize + (neurons * degree)) * time

def barrierMessagesFrac(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

def relaxedGalsMessagesFrac(degree : float, time : int, neurons : int) -> int:
    return neurons * time * (neurons * degree)

def nonSyncedLIAFMessagesFrac(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

def extremeRelaxedLIAFMessagesFrac(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (neurons * degree) * time * fireProb

def galsMessagesFixed(degree : float, time : int, neurons : int) -> int:
    return neurons * time * degree

def clockedMessagesFixed(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * (1 + 2 * neurons + degree) * fireProb * time

def clusterMessagesFixed(degree : float, time : int, neurons : int, fireProb : float, clusterSize : int) -> int:
    return neurons * fireProb * (1 + clusterSize + degree) * time

def barrierMessagesFixed(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * degree * time * fireProb

def relaxedGalsMessagesFixed(degree : float, time : int, neurons : int) -> int:
    return neurons * time * degree

def nonSyncedLIAFMessagesFixed(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * degree * time * fireProb

def extremeRelaxedLIAFMessagesFixed(degree : float, time : int, neurons : int, fireProb : float) -> int:
    return neurons * degree * time * fireProb

degree = 0.2
time = 10000
fireProb = 0.6
clusterNum = 1000

formatter0 = EngFormatter()

x = [i for i in range(1,4*10**5, 100)]
y1 = list(map(lambda el: galsMessagesFrac(degree, time, el), x))
y2 = list(map(lambda el: clockedMessagesFrac(degree, time, el, fireProb), x))
y3 = list(map(lambda el: clusterMessagesFrac(degree, time, el, fireProb, clusterNum), x))
y4 = list(map(lambda el: barrierMessagesFrac(degree, time, el, fireProb), x))
y5 = list(map(lambda el: relaxedGalsMessagesFrac(degree, time, el), x))
y6 = list(map(lambda el: nonSyncedLIAFMessagesFrac(degree, time, el, fireProb), x))
y7 = list(map(lambda el: extremeRelaxedLIAFMessagesFrac(degree, time, el, fireProb), x))
y1f = list(map(lambda el: galsMessagesFixed(degree, time, el), x))
y2f = list(map(lambda el: clockedMessagesFixed(degree, time, el, fireProb), x))
y3f = list(map(lambda el: clusterMessagesFixed(degree, time, el, fireProb, clusterNum), x))
y4f = list(map(lambda el: barrierMessagesFixed(degree, time, el, fireProb), x))
y5f = list(map(lambda el: relaxedGalsMessagesFixed(degree, time, el), x))
y6f = list(map(lambda el: nonSyncedLIAFMessagesFixed(degree, time, el, fireProb), x))
y7f = list(map(lambda el: extremeRelaxedLIAFMessagesFixed(degree, time, el, fireProb), x))

fig = plt.figure()
fig.suptitle("Message Count vs Neuron Count (Izhekevich)", fontsize=16)

ax2 = fig.add_subplot(222)
ax2.set_xlabel("Neuron Count")
ax2.xaxis.set_major_formatter(formatter0)
ax2.set_ylabel("Message Count")
ax2.yaxis.set_major_formatter(formatter0)
firstN = 200
ax2.plot(x[0:firstN], y3[0:firstN], label=f'Clustered ({clusterNum} clusters)')
ax2.plot(x[0:firstN], y6[0:firstN], label='Non-Synchronised Leaky Integrate and Fire')
ax2.plot(x[0:firstN], y7[0:firstN], label='Extreme Relaxed Leaky Integrate and Fire')
ax2.plot(x[0:firstN], y4[0:firstN], ":" ,label='Barrier')
ax2.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for Leaky-Integrate-And-Fire and Barrier)", fontsize=10)
plt.legend()

ax = fig.add_subplot(221)
ax.set_xlabel("Neuron Count")
ax.xaxis.set_major_formatter(formatter0)
ax.set_ylabel("Message Count")
ax.yaxis.set_major_formatter(formatter0)

ax.plot(x, y1, label='GALS')
ax.plot(x, y2, label='Clocked')
ax.plot(x, y3, label=f'Clustered ({clusterNum} clusters)')
ax.plot(x, y4, label='Barrier')
ax.plot(x, y5, label='Relaxed GALS')
ax.plot(x, y6, label='Non-Synchronised Leaky Integrate and Fire')
ax.plot(x, y7, label='Extreme Relaxed Leaky Integrate and Fire')
ax.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for relaxed and normal GALS)", fontsize=10)
plt.legend()

ax4 = fig.add_subplot(224)
ax4.set_xlabel("Neuron Count")
ax4.xaxis.set_major_formatter(formatter0)
ax4.set_ylabel("Message Count")
ax4.yaxis.set_major_formatter(formatter0)
firstN = 200
ax4.plot(x[0:firstN], y3f[0:firstN], label=f'Clustered ({clusterNum} clusters)')
ax4.plot(x[0:firstN], y6f[0:firstN], label='Non-Synchronised Leaky Integrate and Fire')
ax4.plot(x[0:firstN], y7f[0:firstN], label='Extreme Relaxed Leaky Integrate and Fire')
ax4.plot(x[0:firstN], y4f[0:firstN], ":" ,label='Barrier')
ax4.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for Leaky-Integrate-And-Fire and Barrier)", fontsize=10)
plt.legend()

ax3 = fig.add_subplot(223)
ax3.set_xlabel("Neuron Count")
ax3.xaxis.set_major_formatter(formatter0)
ax3.set_ylabel("Message Count")
ax3.yaxis.set_major_formatter(formatter0)

ax3.plot(x, y1f, label='GALS')
ax3.plot(x, y2f, label='Clocked')
ax3.plot(x, y3f, label=f'Clustered ({clusterNum} clusters)')
ax3.plot(x, y4f, label='Barrier')
ax3.plot(x, y5f, label='Relaxed GALS')
ax3.plot(x, y6f, label='Non-Synchronised Leaky Integrate and Fire')
ax3.plot(x, y7f, label='Extreme Relaxed Leaky Integrate and Fire')
ax3.set_title(f"Degree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}\n(Note: Message count identical for relaxed and normal GALS)", fontsize=10)

plt.legend()
fig.subplots_adjust(wspace = 0.3, hspace = 0.4)

yVals = [
    (y1, y1f, "GALS"), 
    (y2, y2f, "Clocked"), 
    (y3, y3f, "Clustered"), 
    (y4, y4f, "Barrier"), 
    (y5, y5f, "Relaxed GALS"), 
    (y6, y6f, "Non-Synchronised Leaky Integrate and Fire"), 
    (y7, y7f, "Extreme Relaxed Leaky Integrate and Fire")
    ]

for y in yVals:
    fig = plt.figure()
    fig.suptitle(f"Message Count vs Neuron Count ({y[2]})", fontsize=16)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_xlabel("Neuron Count")
    ax2.set_xlabel("Neuron Count")
    ax1.xaxis.set_major_formatter(formatter0)
    ax2.xaxis.set_major_formatter(formatter0)
    ax1.set_ylabel("Message Count")
    ax2.set_ylabel("Message Count")
    ax1.yaxis.set_major_formatter(formatter0)
    ax2.yaxis.set_major_formatter(formatter0)
    ax1.set_title(f"Degree as a percentage of all nodes\nDegree = {degree * 100}%, Time steps = {time}, Firing rate = {fireProb}")
    ax2.set_title(f"Fixed Degree\nDegree = {int(degree * 100)}, Time steps = {time}, Firing rate = {fireProb}")
    ax1.plot(x, y[0])
    ax2.plot(x, y[1])


plt.show()


"""
# GALS => t = max (t_synapse + t_return)_0..n
# Clocked => t = max (t_clock1 + max(t_tick_0..n) + max(t_synapse_0..n))
# Clustered => t = max (t_torepeater + max (t_betweenfpga) + max (t_fromrepeater))
# Barrier => t = max(t_synapse_0..n) + k_barrier
# Relaxed GALS => t = max ((t_synapse + t_return)_0..(relaxation * n))
# Non synced Leaky Integrate and Fire => t = max (t_synapse_0..n)
# Extreme Relaxed Leaky Integrate and Fire => t = max (t_synapse_0..n)

ax3 = fig.add_subplot(133)
menMeans = [20, 35, 30, 35, 27, 40, 12]
womenMeans = [25, 32, 34, 20, 25, 26, 27]

ind = range(7)    
width = 0.35       

p1 = ax3.bar(ind, menMeans, width, label='Barrier')
p2 = ax3.bar(ind, womenMeans, width, bottom=menMeans, label='Barxxxxrier')

ax3.set_title("Overheads")
ax3.set_ylabel("Units of time")
plt.legend()


plt.xticks(ind, ('GALS', 'Clocked', 'Clustered', 'Barrier', 'Relaxed GALS', 'Non Synced LIAF', 'Extreme Relaxed LIAF'), rotation=90)

"""