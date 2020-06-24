# figures.py

import matplotlib.pyplot as plt
import numpy as np

# BRIAN

yRunTimeB = [ # run time
    3.7,
    3.05,
    3.96,
    4.17,
    3.55,
    3.96,
     20.1,
    32.47,
    #8840,
]
xDataB = [
    10000,
    64000,
    250000,
    1000000,
    16000000, #4000
    25000000,
     70000000,
    100000000,
    #900000000,
]
yCompileTime = [ # compile time
    0.9, 
    29.85,
    18.19,
    78.85,
    739,
    1164,
     3800,
    4694,
    #41123,
]
"""
fig, ax = plt.subplots(1, 1)
ax.set_title('Time required to run different sized BRIAN networks')
ax.plot(xDataB, yRunTimeB, c='red', marker='^')
ax.set_xscale("log")
ax.grid(which='both')
ax.set_xlabel("Number of synapses")
ax.set_ylabel("Number of seconds to run simulation")
#plt.legend()
plt.show()
"""
# POETS

yRunTime = [ # run time
    11, 
    60+17,
    2*60+2,
    3*60+50,
    622,
    32*60+50,
]

yRunTimeGALS = [ # run time gals
    10, 
    60+10,
    1.9*60+2,
    3*60+30,
    580,
    20*60+5,
]

yRunTimeGALSrel = [ # run time gals relax
    10, 
    60+9,
    1.9*60+5,
    3*60+28,
    587,
    18*60+35,
]

x = [
    10000,
    25000,
    64000,
    1000000,
    5000000,
    10000000,
]

yCompileTimeP = [ # compile time
    4,
    30,
    57,
    2*60+11,
    2120,
    213*60+19,
]


fig, ax = plt.subplots(1, 1)
ax.set_title('Time required to run different sized clocked POETS networks')
ax.plot(x, yRunTime, c='purple', marker='s', label='Clocked')
ax.plot(x, yRunTimeGALS, c='blue', marker='*', label='GALS')
ax.plot(x, yRunTimeGALSrel, c='green', marker='o', label='GALS Relaxed')
#ax.plot([i for i in range(10**4, 10**7, 1000)], [0.000110*i + 70 for i in range(10**4, 10**7, 1000)])
#ax.plot([i for i in range(10**4, 10**7, 1000)], [0.00000000002*i**2 + 70 for i in range(10**4, 10**7, 1000)])
ax.plot(xDataB[:-3], yRunTimeB[:-3], c='red', marker='^', label='Brian Simulator')
ax.set_xscale("log")
ax.grid(which='both')
ax.set_xlabel("Number of synapses")
ax.set_ylabel("Number of seconds to run simulation")
plt.legend()
plt.show()

"""

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Time required to compile different sized POETS and BRIAN networks')
ax1.set_title('All tests')
ax1.plot(x, yCompileTimeP, c='blue', marker='s', label='POETS (clocked)')
ax1.plot(xData, yCompileTime, c='red', marker='^', label='BRIAN')
ax1.set_xscale("log")
ax1.grid(which='both')
ax1.set_xlabel("Number of synapses")
ax1.set_ylabel("Number of seconds to compile model")
ax1.legend()
ax2.set_title('Close up of small networks')
ax2.plot(x[:4], yCompileTimeP[:4], c='blue', marker='s', label='POETS (clocked)')
ax2.plot(xData[:4], yCompileTime[:4], c='red', marker='^', label='BRIAN')
ax2.set_xscale("log")
ax2.grid(which='both')
ax2.set_xlabel("Number of synapses")
ax2.set_ylabel("Number of seconds to compile model")
ax2.legend()
plt.show()





x = [
    100,
    1000,
    5000,
    10000,
    100000,
    500000,
    1000000,
    5000000,
    10000000,
    20000000
]

yBrian = [
    0.3,
    0.45,
    0.5,
    0.6,
    1.3,
    4.2,
    7.98,
    37.8,
    74.6,
    149,
]

yPoets = [
    2*60+11,
    2*60+12,
    2*60+10,
    2*60+10,
    2*60+13,
    2*60+11,
    2*60+11,
    2*60+12,
    2*60+11,
    2*60+12
]

fig, ax = plt.subplots(1, 1)
ax.set_title('Time required to compile different duration POETS and BRIAN networks')
ax.plot(x, yPoets, c='blue', marker='^', label='POETS (10000 synapses)')
ax.plot(x, yBrian, c='red', marker='s', label='BRIAN (10000 synapses)')
ax.set_xscale("log")
ax.grid(which='both')
ax.set_xlabel("Duration to be simulated seconds")
ax.set_ylabel("Number of seconds required to compile")
plt.legend()
plt.show()

x = [
    1000,
    5000,
    10000,
    20000,
    50000,
    75000,
    100000,
    500000,
    1000000
]

y1 = [
    11,
    61,
    85,
    115,
    280,
    401,
    553,
    2408,
    5890
]

y2 = [
    3.2,
    2.98,
    2.97,
    2.93,
    3.57,
    4.31,
    9,
    16.7,
    139,
]

fig, ax = plt.subplots(1, 1)
ax.set_title('Time required to run a 10000 synapse network for various durations')
ax.plot(x, y1, c='blue', marker='^', label='POETS (clocked)')
ax.plot(x, y2, c='red', marker='s', label='BRIAN')
ax.set_xscale("log")
ax.grid(which='both')
ax.set_xlabel("Duration to be simulated seconds")
ax.set_ylabel("Number of seconds required to complete simulation")
plt.legend()
plt.show()
"""