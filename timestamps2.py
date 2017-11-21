import thunderfish.dataloader as dl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


T = 20
lowCriticalFreq = 6000
highCriticalFreq = 10000
with dl.open_data('timestamps2016/trace-1.raw', 0, 60.0) as data:
    Fs = data.samplerate
    dt = 1 / Fs
    nyq = .5 *Fs
    t = np.arange(0, T, dt)
    rawSignal = data[0 : int(T * Fs)]
    a1, b1 = signal.butter(2, [lowCriticalFreq / nyq, highCriticalFreq / nyq], btype='bandpass')
    bandPassSignal = signal.filtfilt(a1, b1, rawSignal)
    squaredSignal = bandPassSignal ** 2
    a2, b2 = signal.butter(2, 10 / nyq, btype='lowpass')
    lowPassSignal = signal.filtfilt(a2, b2, squaredSignal)
    lowPassSignal **= .5

    fig, ax = plt.subplots(3, sharex=True)
    ax[0].plot(t, rawSignal)
    ax[1].plot(t, bandPassSignal)
    ax[2].plot(t, lowPassSignal)
    plt.show()