import os
import thunderfish.dataloader as dl
from scipy import signal
from matplotlib import pyplot as plt


def findFiles(path, ext):
    fileList = []
    print('\nLooking for files with extension ' + ext + ' in ' + path + '...\n')
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                filePath = os.path.join(root, file)
                fileList.append(filePath)
                print('Found: ' + filePath)
    print('\nFound ' + str(len(fileList)) + ' files\nDone!\n')
    return fileList

def LoadRawSignal(path, T):
    print('\nLoading raw file: ' + path + '...')
    with dl.open_data(path) as data:
        Fs = data.samplerate
        rawSignal = data[int(T[0] * Fs) : int(T[1] * Fs)]
        print('Done!\n')
        return Fs, rawSignal

def BandPassFilterRawSignal(rawSignal, Fs, low, high):
    print('\nBand pass filtering raw signal...')
    nyq = Fs / 2
    a, b = signal.butter(2, [low / nyq, high / nyq], btype='bandpass')
    filteredSignal = signal.filtfilt(a, b, rawSignal)
    print('Done!\n')
    return filteredSignal

def CalculateEnvelope(filteredSignal, Fs, low):
    nyq = Fs / 2
    a, b = signal.butter(2, low / nyq, btype='lowpass')
    filteredSignal **= 2
    filteredSignal = signal.filtfilt(a, b, filteredSignal)
    filteredSignal **= .5
    envelope = filteredSignal[0: -1: 35]
    return envelope

def processData(path, T, low, high, lowLow):
    Fs, rawSignal = LoadRawSignal(path, T)
    filteredSignal = BandPassFilterRawSignal(rawSignal, Fs, low, high)
    envelope = CalculateEnvelope(filteredSignal, Fs, lowLow)
    return envelope

rawFilesPath = r'C:\Users\chris\Documents\2016'
T = (0, 500)
low = 6000
high = 10000
lowLow = 10
rawFilesList = findFiles(rawFilesPath, '.raw')
for rawFile in rawFilesList:
    envelope = processData(rawFile, T, low, high, lowLow)
    plt.plot(envelope)
    plt.title(rawFile)
    plt.show()
    ans = input('Continue?')
    if ans == 'no':
        break