import thunderfish.dataloader as dl
import matplotlib.pyplot as plt
from scipy import signal

with dl.open_data('timestamps2016/trace-1.raw', 0, 60.0) as data:
    dataPart = data[0 : 100000]
    sampleRate = data.samplerate
    plt.psd(dataPart, Fs=sampleRate, NFFT=1024)
    plt.show()
    nyq = .5 * sampleRate
    low = 6000/nyq
    high = 8000/nyq
    b, a = signal.butter(2, [low, high], btype='bandpass')
    y = signal.filtfilt(b, a, dataPart)
    plt.psd(y, Fs=sampleRate, NFFT=1024)
    plt.show()