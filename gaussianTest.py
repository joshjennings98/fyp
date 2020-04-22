# gaussianTest.py

import numpy as np
import matplotlib.pyplot as plt

"""
uint32_t urng(uint32_t &state)
    {
      state = state*1664525+1013904223;
      return state;
    }

float grng(uint32_t &state)
{
    uint32_t u=urng(state);
    int32_t acc=0;
    for(unsigned i=0;i<8;i++){
    acc += u&0xf;
    u=u>>4;
    }
    // a four-bit uniform has mean 7.5 and variance ((15-0+1)^2-1)/12 = 85/4
    // sum of four uniforms has mean 8*7.5=60 and variance of 8*85/4=170
    const float scale=0.07669649888473704; // == 1/sqrt(170)
    return (acc-60.0f) * scale;
}
"""

def urng(state : np.uint32) -> np.uint32:
    return state * 1664525 + 1013904223

def grng(state : np.uint32) -> float:
    u : np.uint32 = urng(state)
    acc : np.uint32 = 0

    for _ in range(8):
        acc += u & 0xf
        u = u >> 4

    # a four-bit uniform has mean 7.5 and variance ((15-0+1)^2-1)/12 = 85/4
    # sum of four uniforms has mean 8*7.5=60 and variance of 8*85/4=170
    scale : float = 0.07669649888473704 # == 1/sqrt(170)
    
    return (acc - 60.0) * scale

np.random.seed(123)
data = []
tests = 10000000 #2**32-1
onePercent = tests / 100

for i in range(tests):
    x = np.random.randint(0, 2**32-1)
    data.append(grng(x)) # data.append(grng(i))
    if i % onePercent == 0:
        print(f"Completed {100*i//tests}%")
print(f"Completed 100%")

fig, axis = plt.subplots(1, 3)

axis[0].hist(data, color = 'black', bins = 100)
axis[1].hist(data, color = 'black', bins = 200)
axis[2].hist(data, color = 'black', bins = 500)

plt.suptitle(f"Distribution of grng() for {tests} uniform random seeds\n\nμ = {np.mean(data)}        σ² = {np.var(data)}")
axis[0].set_title("Bins = 100")
axis[1].set_title("Bins = 200")
axis[2].set_title("Bins = 500")

for i in range(3):
    axis[i].set_xlabel("x")
    axis[i].set_ylabel("Density")

plt.show()
