import thunderfish.dataloader as dl
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt

def LoadRawSignal(path, T):
    with dl.open_data(path) as data:
        Fs = data.samplerate
        rawSignal = data[int(T[0] * Fs) : int(T[1] * Fs)]
        return Fs, rawSignal


def BandPassFilterRawSignal(rawSignal, Fs, low, high):
    nyq = Fs / 2
    a, b = signal.butter(2, [low / nyq, high / nyq], btype='bandpass')
    filteredSignal = signal.filtfilt(a, b, rawSignal)
    return filteredSignal

def CalculateEnvelope(filteredSignal, Fs, low):
    nyq = Fs / 2
    a, b = signal.butter(2, low / nyq, btype='lowpass')
    filteredSignal **= 2
    filteredSignal = signal.filtfilt(a, b, filteredSignal)
    filteredSignal **= .5
    envelope = filteredSignal[0: -1: 35]
    return envelope

def findThresholdCrossings(curve, thresh):
    starts = []
    ends = []
    n0 = 0
    for i, n in enumerate(curve):
        if n0 < thresh and n > thresh:
            starts.append(i)
        elif n0 > thresh and n < thresh:
            ends.append(i)
        n0 = n
    return starts, ends

def plot(T, Fs, rawSignal, envelope, startTimeSongs, endTimeSongs):
    tRaw = np.arange(T[0], T[1], 1 / Fs)
    tEnvelope = tRaw[0: -1: 35]
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(tRaw, rawSignal)
    ax[1].plot(tEnvelope, envelope)
    for i in range(len(startTimeSongs)):
        ax[1].plot(tEnvelope[startTimeSongs[i]: endTimeSongs[i]], envelope[startTimeSongs[i]: endTimeSongs[i]], 'r')
    plt.show()

path = 'C:/Users/chris/Documents/2016/2016-07-24-1005/trace-3.raw'
T = (0, 100)
lowBand = 6000
highBand = 10000
lowLow = 5
threshSongDetect = .01
Fs, rawSignal = LoadRawSignal(path, T)
filteredSignal = BandPassFilterRawSignal(rawSignal, Fs, lowBand, highBand)
envelope = CalculateEnvelope(filteredSignal, Fs, 10)
startTimeSongs, endTimeSongs = findThresholdCrossings(envelope, threshSongDetect)
plot(T, Fs, rawSignal, envelope, startTimeSongs, endTimeSongs)