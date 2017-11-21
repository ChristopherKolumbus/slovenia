import numpy as np

from matplotlib import pyplot as plt

a = np.array([0, 0, 0, 1, 2, 1, 0, 0, 0])
b = np.array([0, 0, 0, 0, 1, 2, 1, 0, 0])

c = np.correlate(a, b, 'full')
plt.plot(c)
plt.show()