import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
fig, axis = plt.subplots(1, 1)

axis.set_title("Hardware Barrier Clocked Model")
axis.set_xlabel("Time Step")
axis.set_ylabel("Neuron")

axis.grid(which='both', axis='both')
axis.set_xticks([0, 1, 1.25, 2.25, 2.5, 3.5, 3.75])
plt.xticks(rotation=70)
axis.set_yticks([i for i in range(0, 7)])

p1 = [
    [0, 0],
    [1, 1],
    [0, 5],
    [1, 1],
    [1, 3],
    [1, 6],
    [1, 1],
    [1.25, 1],
    [1.25, 3],
    [1.25, 6],
]
p2 = [
    [1.25, 1],
    [1.25, 3],
    [1.25, 6],
    [2.25, 1],
    [2.25, 3],
    [2.25, 0],
    [2.25, 1],
    [2.5, 1],
    [2.5, 3],
    [2.5, 5],
    [3.5, 2],
    [3.5, 4],
    [3.5, 6]
]
x, y = zip(*p1)
axis.scatter(x, y, zorder=10, c='black', s=100)
x, y = zip(*p2)
axis.scatter(x, y, zorder=10, c='black', s=100)

x, y = zip(*[p1[0], p1[4]])
axis.plot(x, y, c='red', label='Fired Spike')
x, y = zip(*[p1[0], p1[3]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[-1], p2[4]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[-3], p2[5]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[2], p1[5]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[2], p1[4]])
axis.plot(x, y, c='red')
x, y = zip(*[p1[-2], p2[3]])
axis.plot(x, y, c='red')

x, y = zip(*[p2[0], p2[4]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[0], p2[3]])
axis.plot(x, y, c='red')

x, y = zip(*[p2[10], p2[7]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[10], p2[8]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[11], p2[8]])
axis.plot(x, y, c='red')
x, y = zip(*[p2[12], p2[9]])
axis.plot(x, y, c='red')

rectangle = plt.Rectangle((1, -1), 0.25, 8, fc='cyan', zorder=9)
plt.gca().add_patch(rectangle)
rectangle = plt.Rectangle((2.25, -1), 0.25, 8, fc='cyan', zorder=9)
plt.gca().add_patch(rectangle)
rectangle = plt.Rectangle((3.5, -1), 0.25, 8, fc='cyan', zorder=9)
plt.gca().add_patch(rectangle)

plt.text(1.07, 2.25, "Hardware Idle", c="black", fontsize=12, zorder=12, rotation=90)
plt.text(2.32, 2.25, "Hardware Idle", c="black", fontsize=12, zorder=12, rotation=90)
plt.text(3.57, 2.25, "Hardware Idle", c="black", fontsize=12, zorder=12, rotation=90)

plt.legend(fontsize='large').set_zorder(11)

axis.set_xlim(-0.2, 4)
axis.set_ylim(-0.2, 6.2)

plt.show()