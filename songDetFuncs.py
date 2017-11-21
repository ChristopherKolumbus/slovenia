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
    envelope = filteredSignal ** 2
    nyq = Fs / 2
    a, b = signal.butter(2, low / nyq, btype='lowpass')
    envelope = signal.filtfilt(a, b, envelope)
    envelope = envelope ** .5
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