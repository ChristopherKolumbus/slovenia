import shelve
import numpy as np

from matplotlib import pyplot as plt


with shelve.open(r'C:\Users\chris\Documents\calltiming_17_11_21\data') as d:
    t1 = d['0. trace']['CallStart']
    t2 = d['1. trace']['CallStart']

fs = 1000
dt = 1 / fs
sig = .4
mini = np.minimum(t1[0], t2[0])
t1 -= mini
t2 -= mini
dur = np.ceil(np.maximum(t1[-1], t2[-1]))
v1 = np.zeros(dur.astype(int) * fs)
v2 = np.copy(v1)
v1[np.round(t1 * fs).astype(int)] += 1
v2[np.round(t2 * fs).astype(int)] += 1
x = np.arange(-5 * sig, 5 * sig, dt)
y = np.exp(-np.power(x, 2) / (2*np.power(sig, 2)))
v1 = np.convolve(y, v1)
v2 = np.convolve(y, v2)
v2_part = v2[:np.round(.1 * v2.shape[0]).astype(int)]
corr = np.correlate(v1 - v1.mean(), v2_part - v2_part.mean(), mode='valid') / (v1.std() * v2_part.std()) / v1.shape[0]

fig, ax = plt.subplots(2)
#ax[0].plot(v1)
#ax[0].plot(v2)
plt.plot(corr)
plt.show()