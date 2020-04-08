# test_model.py

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(123)

Ne = 800
Ni = 200

re = np.random.uniform(0, 1, Ne)
ri = np.random.uniform(0, 1, Ni)

a = np.concatenate([0.02 * np.ones(Ne), 0.02 + 0.08 * ri])
b = np.concatenate([0.2 * np.ones(Ne), 0.25 - 0.05 * ri])
c = np.concatenate([-65 + 15 * np.square(re), -65 * np.ones(Ni)])
d = np.concatenate([8 - 6 * np.square(re), 2 * np.ones(Ni)])

S = np.concatenate([0.5 * np.random.uniform(0, 1, (Ne, Ne + Ni)), -1 * np.random.uniform(0, 1, (Ni, Ne + Ni))])

v = -65 * np.ones(Ne + Ni)
u = b * v

firings = np.column_stack((np.zeros(1), np.zeros(1)))

epochs = 200

for t in range(epochs):
    I = np.concatenate([5 * np.random.normal(0, 1, Ne), 2 * np.random.normal(0, 1, Ni)])
    fired = np.argwhere(v >= 30).flatten()
    tempFirings = np.column_stack((t + 0 * fired, fired))
    firings = np.concatenate([firings, tempFirings])

    v[fired] = c[fired]

    u[fired] = u[fired] + d[fired]

    temp = []

    for i, x in enumerate(S):
        if i in fired:
            temp.append(sum(x))
        else:
            temp.append(0)

    I = I + temp

    v = v + 0.5 * (0.04 * np.square(v) + 5 * v + 140 - u + I)  # step 0.5 ms
    v = v + 0.5 * (0.04 * np.square(v) + 5 * v + 140 - u + I)  # for numerical
    u = u + a * (b * v - u)                                    # stability

firings = firings[1:]

fig, (axis1, axis2) = plt.subplots(1, 2)
fig.suptitle("Plot of which neurons are firing at each epoch")

axis1.scatter(firings[:,0], firings[:,1], s=1)
axis1.set_xlim(0, epochs)
axis1.set_ylim(0, Ne+Ni)

axis1.set_xlabel("Epoch")
axis1.set_ylabel("Neuron")
axis1.set_title("Test")

newFiringsX = range(epochs)
newFiringsY = [0] * epochs

for i in firings:
    newFiringsY[int(i[0])] += 1

axis2.plot(newFiringsX, newFiringsY)
axis2.set_xlim(0, epochs)
axis2.set_ylim(0, Ne+Ni)

axis2.set_xlabel("Epoch")
axis2.set_ylabel("Neuron")
axis2.set_title("Test")

plt.show()
