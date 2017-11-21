import shelve
import numpy as np

from matplotlib import pyplot as plt


def gaussian(x, sig):
    return np.exp(-np.power(x, 2.) / (2*np.power(sig, 2.)))


with shelve.open(r'C:\Users\chris\Documents\calltiming_17_11_21\data') as d:
    call_start_1 = d['0. trace']['CallStart']
    call_start_2 = d['1. trace']['CallStart']

sampling_rate = 1000
dt = 1/sampling_rate
minimum = np.floor(np.min(np.concatenate((call_start_1, call_start_2))))
call_start_1 = call_start_1 - minimum
call_start_2 = call_start_2 - minimum
session_length = np.ceil(np.max(np.concatenate((call_start_1, call_start_2)))).astype(int)
logical_array_1 = np.zeros((session_length * sampling_rate)).astype(int)
logical_array_2 = np.copy(logical_array_1)
for n in call_start_1:
    logical_array_1[np.round(n * 1000).astype(int)] += 1
for n in call_start_2:
    logical_array_2[np.round(n * 1000).astype(int)] += 1
sigma = .4
x_gauss = np.arange(-5 * sigma, 5 * sigma, dt)
y_gauss = gaussian(x_gauss, .4)
logical_array_1 = np.convolve(y_gauss, logical_array_1)
logical_array_2 = np.convolve(y_gauss, logical_array_2)
print(np.correlate(logical_array_1, logical_array_2))
plt.plot(logical_array_1)
plt.plot(logical_array_2)
plt.show()
