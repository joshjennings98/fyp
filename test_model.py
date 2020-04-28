# test_model.py

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(123)

Ne = 800
Ni = 200

epochs = 1000

re = np.random.uniform(0, 1, Ne)
ri = np.random.uniform(0, 1, Ni)

a = np.concatenate([0.02 * np.ones(Ne), 0.02 + 0.08 * ri])
b = np.concatenate([0.2 * np.ones(Ne), 0.25 - 0.05 * ri])
c = np.concatenate([-65 + 15 * np.square(re), -65 * np.ones(Ni)])
d = np.concatenate([8 - 6 * np.square(re), 2 * np.ones(Ni)])

S = np.concatenate([0.5 * np.random.uniform(0, 1, (Ne, Ne + Ni)), -1 * np.random.uniform(0, 1, (Ni, Ne + Ni))])

v = -65 * np.ones(Ne + Ni)
u = b * v

firings = []

for t in range(epochs):
    I = np.concatenate([5 * np.random.normal(0, 1, Ne), 2 * np.random.normal(0, 1, Ni)])
    fired = np.argwhere(v >= 30).flatten()
    
    firings.append(list(fired))

    v[fired] = c[fired]
    u[fired] = u[fired] + d[fired]

    I += np.sum(S[fired],axis=0)

    v = v + 1 * (0.04 * v * v + 5 * v + 140 - u + I)  # step 0.5 ms
    #v = v + 0.5 * (0.04 * v * v + 5 * v + 140 - u + I)  # for numerical

    u = u + a * (b * v - u)                                    # stability

"""
fig, (axis1, axis2) = plt.subplots(1, 2)
fig.suptitle("Plot of which neurons are firing at each epoch")

axis1.plot(range(epochs), list(map(lambda l: len(l), firings)))
axis1.set_xlim(0, epochs)
axis1.set_ylim(0, Ne+Ni)

axis1.set_xlabel("Epoch")
axis1.set_ylabel("Number of firing neurons")
axis1.set_title("Quantity of neurons firing")

firings = list(zip(range(epochs), firings))
firings = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings))
firings = list(filter(lambda l: l != [], firings))
firings = [j for i in firings for j in i]

ydata, xdata = zip(*firings)

axis2.scatter(xdata, ydata, s=1)
axis2.set_xlim(0, epochs)
axis2.set_ylim(0, Ne+Ni)

axis2.set_xlabel("Epoch")
axis2.set_ylabel("Neuron")
axis2.set_title("When each neuron fires")

plt.show()
"""

fig, axis = plt.subplots(1, 1)
fig.suptitle("Plot of which neurons are firing at each epoch")

axis.plot(range(epochs), list(map(lambda l: len(l), firings)))
axis.set_xlim(0, epochs)
axis.set_ylim(0, Ne+Ni)

axis.set_xlabel("Epoch")
axis.set_ylabel("Number of firing neurons")
axis.set_title("Quantity of neurons firing")

plt.show()

fig, axis = plt.subplots(1, 1)

firings = list(zip(range(epochs), firings))
firings = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings))
firings = list(filter(lambda l: l != [], firings))
firings = [j for i in firings for j in i]

ydata, xdata = zip(*firings)

axis.scatter(xdata, ydata, s=1)
axis.set_xlim(0, epochs)
axis.set_ylim(0, Ne+Ni)

axis.set_xlabel("Epoch")
axis.set_ylabel("Neuron")
axis.set_title("When each neuron fires")

plt.show()