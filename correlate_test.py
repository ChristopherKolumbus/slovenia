import numpy as np

from  matplotlib import pyplot as plt


fs = 1000
dt = 1 / fs
sig = .4
t1 = np.arange(0, 100, 5, dtype=float)
t2 = np.arange(0, 100, 5, dtype=float)
t1 += np.random.rand(t1.shape[0]) * 2
t2 += np.random.rand(t2.shape[0]) * 2
mini = np.minimum(t1[0], t2[0])
t1 -= mini
t2 -= mini
dur = np.ceil(np.maximum(t1[-1], t2[-1])) + 1
l1 = np.zeros(dur.astype(int) * fs)
l2 = np.copy(l1)
l1[np.round(t1 * fs).astype(int)] += 1
l2[np.round(t2 * fs).astype(int)] += 1
x = np.arange(-5 * sig, 5 * sig, dt)
y = np.exp(-np.power(x, 2) / (2*np.power(sig, 2)))
l1 = np.convolve(y, l1)
l2 = np.convolve(y, l2)
l2_part = l2[:round(.5 * len(l2))]
print(l2_part)
corr = np.correlate(l1 - l1.mean(), l2_part - l2_part.mean(), mode='valid') / (l1.std() * l2_part.std()) / l1.shape[0]
#corr = np.correlate(l1 - l1.mean(), l2 - l2.mean(), mode='full') / (l1.std() * l2.std()) / l1.shape[0]

fig, ax = plt.subplots(2)
ax[0].plot(l1)
ax[0].plot(l2)
ax[1].plot(corr)
plt.show()
