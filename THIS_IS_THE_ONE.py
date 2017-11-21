import numpy as np


from matplotlib import pyplot as plt

from thunderfish import dataloader as dl


with dl.open_data(r'C:\Users\chris\Documents\plittoralis-timestamps\recordings\2015-07-29-aa\trace-6.raw') as data:
    fs = data.samplerate
    data = data[0, 100]
dt = 1 / fs
plt.plot(np.arange(data.shape[0]) * dt, data)
plt.show()