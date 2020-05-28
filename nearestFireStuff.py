import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np

numEpochs = 1000
numNeurons = 100

firings1 = np.load('data.npy', allow_pickle=True)
firings2 = np.load('dataHardwareFires.npy', allow_pickle=True)

# dataset 1 fix
firings1 = list(zip(range(-1, numEpochs-1, 1), firings1))
firings1 = list(map(lambda t: list(map(lambda x: (x, t[0]), t[1])), firings1))
firings1 = list(filter(lambda l: l != [], firings1))
firings1 = [j for i in firings1 for j in i]

# dataset 2
xdata, ydata = zip(*firings2)

#plt.show()

fig, axis = plt.subplots(1, 1)
fig.suptitle("Plot of the neurons that fire per epoch")
axis.set_title("Distance between hardware fire and closest numpy sim fire")
axis.set_xlabel("Epoch")
axis.set_ylabel("Neuron")

error = [0 for _ in range(numEpochs)]

# Note reason it looks like some dots aren't connected is because those aren't the closest fires
# The reason some blues look linked is because they are both linked to an orange in between them or beneath one of them
for idx in range(numNeurons):
    ydata1, xdata1 = zip(*list(filter(lambda x: x[0] == idx, firings1)))
    xdata2, ydata2 = zip(*list(filter(lambda x: x[1] == idx, firings2)))

    for i in range(min(len(xdata1), len(xdata2))):
        #print(xdata1[i])
        given_value = xdata1[i]
        absolute_difference_function = lambda list_value : abs(list_value - given_value)
        closest_value = min(xdata2, key=absolute_difference_function)
        plt.plot([given_value, closest_value], [ydata1[i], ydata2[i]], 'k', zorder=0, label="Nearest fire" if idx == 1 and i == 0 else "")

        error[xdata1[i]] += abs(given_value - closest_value)

    axis.scatter(xdata2, ydata2, s=4, color='orange', zorder=1, label="NumPy sim fires" if idx == 0 else "")
    axis.scatter(xdata1, ydata1, s=4, color='blue', zorder=1, label="Hardware fires" if idx == 0 else "")

axis.set_xlim(0, numEpochs)
axis.set_ylim(0, numNeurons)
axis.legend(loc='upper center', bbox_to_anchor=(0.1, 0.15), shadow=True, ncol=1)

#plt.show()

fig, axis = plt.subplots(1, 1)
fig.suptitle("Absolute error in timesteps between neurons firing in the NumPy simulation and Hardware")

axis.set_title("Error in fires")
axis.set_xlabel("Epoch")
axis.set_ylabel("Error")

axis.plot(range(numEpochs), error, label='Absolute Error')

def test_func(x, a, b):
    return a * np.tanh(b * x)

params, params_covariance = optimize.curve_fit(test_func, range(numEpochs), error) # p0=[2, 2], 

numZeroError = 0
for i in error:
    if i == 0:
        numZeroError += 1
    else:
        break

yrange = test_func(range(numEpochs), params[0], params[1])

plt.plot(np.array(range(numEpochs)), [0 if i < numZeroError else yrange[i - numZeroError] for i in range(numEpochs)], label='Fitted function', color='red')

plt.legend(loc='best')

plt.show()

axis.set_xlim(0, numEpochs)
axis.set_ylim(0, max(error))

plt.show()