import numpy as np
import random
import matplotlib.pyplot as plt

"""
To explain this look at pairwise summation.
This is important in why order of the neurons matters
"""

xData, yData1, yData2 = [], [], []

for size in range(1, 8):
    print("List of size", size)

    np.random.seed(123)
    random.seed(123)

    x = np.random.uniform(0, 1, 10 ** size)
    y = np.random.uniform(0, 1, 10 ** size)

    z1 = x + y

    np.random.seed(123)
    random.seed(123)

    x = np.random.uniform(0, 1, 10 ** size)
    y = np.random.uniform(0, 1, 10 ** size)

    np.random.shuffle(x)
    np.random.shuffle(y)

    z2 = x + y

    numpyError = abs(np.sum(z1) - np.sum(z2))
    normalError = abs(sum(z1) - sum(z2))
    
    xData.append(size)
    yData1.append(normalError)
    yData2.append(numpyError)

    print("Error (normal sum)", normalError)
    print("Error (np.sum)", numpyError, end='\n\n')

fig, (axis1, axis2) = plt.subplots(1, 2)
fig.suptitle("Error in summation functions when order of array elements is changed")

axis1.set_xlabel("Array Length (10 ^ x)")
axis1.set_ylabel("Absolute Error")
axis1.set_title("Python sum()")
axis1.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

axis2.set_xlabel("Array Length (10 ^ x)")
axis2.set_ylabel("Absolute Error")
axis2.set_title("numpy.sum()")
axis2.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

axis1.plot(xData, yData1)
axis2.plot(xData, yData2, c="red")

plt.show()