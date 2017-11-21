import songDetFuncs
import numpy as np
from matplotlib import pyplot as plt

path = r'C:\Users\chris\Documents\2016\2016-07-24-0853\trace-3.raw'

T = (0, 100)
bandpassLow = 6000
bandpassHigh = 10000
lowpassLow = 5
threshold = .005
size = 1
Fs, rawSignal = songDetFuncs.LoadRawSignal(path, T)
filteredSignal = songDetFuncs.BandPassFilterRawSignal(rawSignal, Fs, bandpassLow, bandpassHigh)
envelope = songDetFuncs.CalculateEnvelope(filteredSignal, Fs, lowpassLow)
allStarts, allEnds = songDetFuncs.findThresholdCrossings(envelope, threshold)
print(len(allStarts))

for i in range(len(allStarts)):
    callStart = allStarts[i]
    callEnd = allEnds[i]
    time = np.arange(0, callEnd - callStart) / Fs
    envelopePart = envelope[callStart: callEnd]
    filteredSignalPart = filteredSignal[callStart: callEnd]
    timeWindow = np.arange(-round(size * Fs), filteredSignalPart.shape[0] + round(size * Fs)) / Fs
    if callStart - round(size * Fs) < 0:
        winStart = 0
    else:
        winStart = callStart - round(size * Fs)
    timeWindow = np.arange(-round(siz, filteredSignalPart.shape[0] + ro)
    envelopeWindow = envelope[winStart: callEnd + round(size * Fs)]
    filteredSignalWindow = filteredSignal[callStart - round(size * Fs): callEnd + round(size * Fs)]
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(timeWindow, envelopeWindow, 'g')
    ax[0].plot(time, envelopePart, 'r')
    ax[1].plot(timeWindow, filteredSignalWindow, 'g')
    ax[1].plot(time, filteredSignalPart, 'r')
    plt.show()