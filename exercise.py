import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

dt = 0.0001
sampleRate = int(1 / dt)
fSin = 600
tSin = np.arange(0, 1, dt)
ySin = np.sin(2 * np.pi * fSin * tSin)
t = np.arange(0, 20, dt)
y = np.zeros(len(t))
for i in range(0, 20, 2):
    y[i * sampleRate : i * sampleRate + len(tSin)] = ySin
yLowPass = y ** 2
nyq = .5 * sampleRate
b, a = signal.butter(2, 100 / nyq, btype='lowpass')
yLowPass = signal.filtfilt(b, a, yLowPass)
yLowPass = np.sqrt(yLowPass)

# square root
fig, ax = plt.subplots(2, 2)
ax[0, 0].plot(t, y)
ax[0, 1].plot(t, yLowPass)
ax[1, 0].psd(y, Fs=sampleRate, NFFT=1024)
ax[1, 1].psd(yLowPass, Fs=sampleRate, NFFT=1024)
plt.show()