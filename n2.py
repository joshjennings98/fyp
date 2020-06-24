import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
fig, axis = plt.subplots(1, 1)

axis.set_title("Clock Neuron Model")
axis.set_xlabel("Time Step")
axis.set_ylabel("Neuron")

axis.grid(which='both', axis='both')
axis.set_xticks([i for i in range(0, 6)])
axis.set_yticks([i for i in range(0, 7)])

c = [
    [1, 0],
    [3, 0],
]

p1 = [
    [0, 4],
    [4, 4],
    [5, 3],
    [5, 5]
]
p2 = [
    [2, 1],
    [2, 2],
    [2, 3],
    [2, 4],
    [2, 5],
    [2, 6],
]

x, y = zip(*p1)
axis.scatter(x, y, zorder=10, c='black', s=100)
x, y = zip(*p2)
axis.scatter(x, y, zorder=10, c='black', s=100)
x, y = zip(*c)
axis.scatter(x, y, zorder=10, c='purple', s=100)

x, y = zip(*[p2[0], c[1]])
axis.plot(x, y, c='blue', label='Neurons Ping Clock')
x, y = zip(*[p2[0], c[0]])
axis.plot(x, y, c='cyan', label='Clock Ping Neurons')
x, y = zip(*[p1[1], p1[2]])
axis.plot(x, y, c='red', label='Fired Spike')
x, y = zip(*[p1[1], p1[3]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[0], c[0]])
axis.plot(x, y, c='blue')

x, y = zip(*[p2[1], c[0]])
axis.plot(x, y, c='cyan')
x, y = zip(*[p2[2], c[0]])
axis.plot(x, y, c='cyan')
x, y = zip(*[p2[3], c[0]])
axis.plot(x, y, c='cyan')
x, y = zip(*[p2[4], c[0]])
axis.plot(x, y, c='cyan')
x, y = zip(*[p2[5], c[0]])
axis.plot(x, y, c='cyan')

x, y = zip(*[p2[1], c[1]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[2], c[1]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[3], c[1]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[4], c[1]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[5], c[1]])
axis.plot(x, y, c='blue')

x, y = zip(*[p1[1], c[1]])
axis.plot(x, y, c='cyan')


plt.legend(fontsize='large')

axis.set_xlim(-0.2, 5.2)
axis.set_ylim(-0.2, 6.2)

plt.show()