import os
import thunderfish.dataloader as dl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def FindRawFiles(path):
    data = []
    for file in os.listdir(path):
        if file.endswith('.raw'):
            data.append(dict([('name', file), ('path', path)]))
    return data
def GetRawSignal(data, T):
    for i, trace in enumerate(data):
        with dl.open_data(os.path.join(trace['path'], trace['name'])) as rawSignal:
            data[i]['Fs'] = rawSignal.samplerate
            data[i]['rawSignal'] = rawSignal[0: int(T * data[i]['Fs'])]
    return data

path = 'C:/Users/chris/Documents/timestamps2016'
data = FindRawFiles(path)
T = 20
GetRawSignal(data, T)
Fs = data[0]['Fs']
nyq = Fs / 2
low = 6000
high = 10000
a, b = signal.butter(2, [low / nyq, high / nyq], btype='bandpass')
for i, trace in enumerate(data):
    data[i]['filteredSignal'] = signal.filtfilt(a, b, data[i]['rawSignal'])

t = np.arange(0, T, 1 / data[0]['Fs'])
fig, ax = plt.subplots(2, 3, sharex=True)
ax[0, 0].plot(t, data[0]['filteredSignal'])
ax[0, 1].plot(t, data[1]['filteredSignal'])
ax[0, 2].plot(t, data[2]['filteredSignal'])
ax[1, 0].plot(t, data[3]['filteredSignal'])
ax[1, 1].plot(t, data[4]['filteredSignal'])
ax[1, 2].plot(t, data[5]['filteredSignal'])
plt.show()