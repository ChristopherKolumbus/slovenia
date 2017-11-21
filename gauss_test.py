import numpy as np

from matplotlib import pyplot as plt

fs = 40000
dt = 1 / fs
sigma = .4

def gaussian(x, sig):
    return np.exp(-np.power(x, 2.) / (2*np.power(sig, 2.)))

x = np.arange(-5 * sigma, 5 * sigma, dt)
y = gaussian(x, sigma)
y_norm = y / np.sum(y)

#plt.plot(x, y)
plt.plot(x, y_norm)
plt.show()