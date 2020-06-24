import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
fig, axis = plt.subplots(1, 1)

axis.set_title("Globally-Asynchronous Locally-Synchronous Model")
axis.set_xlabel("Time Step")
axis.set_ylabel("Neuron")

axis.grid(which='both', axis='both')
axis.set_xticks([i for i in range(0, 5)])
axis.set_yticks([i for i in range(0, 7)])

p1 = [
    [0, 1],
    [0, 3],
    [0, 5],
    [1, 1],
    [1, 3],
    [1, 6],
    [1, 4],
    [2, 1],
    [2, 3],
    [2, 5],
]
p2 = [
    [2, 1],
    [2, 3],
    [2, 5],
    [3, 1],
    [3, 3],
    [3, 6],
    [3, 4],
    [4, 1],
    [4, 3],
    [4, 5],
]
x, y = zip(*p1)
axis.scatter(x, y, zorder=10, c='black', s=100)
x, y = zip(*p2)
axis.scatter(x, y, zorder=10, c='black', s=100)

x, y = zip(*[p1[0], p1[4]])
axis.plot(x, y, c='red', label='Fired Spike')
x, y = zip(*[p1[0], p1[3]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[1], p1[4]])
axis.plot(x, y, c='blue', label="Didn't Fire Spike")
x, y = zip(*[p1[1], p1[6]])
axis.plot(x, y, c='blue')
x, y = zip(*[p1[2], p1[5]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[2], p1[4]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[3], p1[7]])
axis.plot(x, y, c='blue')
x, y = zip(*[p1[4], p1[7]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[4], p1[8]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[4], p1[9]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[5], p1[9]])
axis.plot(x, y, c='blue')
x, y = zip(*[p1[6], p1[8]])
axis.plot(x, y, c='blue')

x, y = zip(*[p2[0], p2[4]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[0], p2[3]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[1], p2[4]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[1], p2[6]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[2], p2[5]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[2], p2[4]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[3], p2[7]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[4], p2[7]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[4], p2[8]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[4], p2[9]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[5], p2[9]])
axis.plot(x, y, c='blue')
x, y = zip(*[p2[6], p2[8]])
axis.plot(x, y, c='blue')

plt.legend(fontsize='large')

axis.set_xlim(-0.2, 4.2)
axis.set_ylim(-0.2, 6.2)

plt.show()