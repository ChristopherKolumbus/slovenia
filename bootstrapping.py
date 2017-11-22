import shelve
import numpy as np

from matplotlib import pyplot as plt


def gen_new_times(times):
    diffs = np.diff(times - np.min(times))
    new_times = np.zeros(times.shape)
    for i in range(new_times.shape[0] - 1):
        new_times[i + 1] = new_times[i] + np.random.choice(diffs)
    return new_times


with shelve.open(r'..\..\Documents\calltiming_17_11_21\data') as d:
    call_start_1 = d['0. trace']['CallStart']
call_start_new = gen_new_times(call_start_1)
means = np.zeros(10000)
for n in range(10000):
    means[n] = np.mean(gen_new_times(call_start_1))
plt.plot(means, 'bo')
plt.show()
