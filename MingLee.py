import numpy as np

from scipy import signal
from matplotlib import pyplot as plt

from thunderfish import dataloader as dl


def load_raw(data_path, win):
    with dl.open_data(data_path) as data_file:
        fs = data_file.samplerate
        data = np.array(data_file[round(win[0] * fs):round(win[1] * fs)])
        return fs, data


def filter_raw(data, fs, low_lim, high_lim):
    nyq = fs / 2
    b, a = signal.butter(2, [low_lim / nyq, high_lim / nyq], btype='bandpass')
    return signal.filtfilt(b, a, data)

def calc_envelope(data, fs, low_lim):
    nyq = fs / 2
    data = data ** 2
    b, a = signal.butter(2, low_lim / nyq, btype='lowpass')
    return np.sqrt(signal.filtfilt(b, a, data))


def norm_data(data):
    return (data-np.min(data)) / (np.max(data)-np.min(data))


def find_crossings(data, threshold):
    n0 = 0
    up = []
    down = []
    for i, n in enumerate(data):
        if n0 < threshold < n:
            up.append(i)
        elif n0 > threshold > n:
            down.append(i)
        n0 = n
    if len(up) > len(down):
        del up[-1]
    elif len(up) < len(down):
        del down[0]
    return np.array(up), np.array(down)


def calc_amplitude(data, up, down):
    amplitudes = np.zeros(up.shape[0])
    for i, (n1, n2) in enumerate(zip(up, down)):
        amplitudes[i] = np.max(data[n1:n2])
    return  amplitudes


raw_data_path = r'E:\Christoph\Documents\timestamps\trace-2.raw'
time_window = (0, -1)
sampling_rate, raw_data = load_raw(raw_data_path, time_window)
filtered_signal = filter_raw(raw_data, sampling_rate, 6000, 10000)
signal_envelope = np.nan_to_num(calc_envelope(filtered_signal, sampling_rate, 3)[::round(sampling_rate / 1000)])
signal_envelope = norm_data(signal_envelope)
envelope_threshold = .2
start, stop = find_crossings(signal_envelope, envelope_threshold)
call_amplitudes = calc_amplitude(signal_envelope, start, stop)


t = np.arange(raw_data.shape[0]) / sampling_rate
t_envelope = np.arange(signal_envelope.shape[0]) / 1000
#plt.plot(t_envelope, signal_envelope)
#plt.plot(t_envelope[start], signal_envelope[start], 'go')
#plt.plot(t_envelope[stop], signal_envelope[stop], 'ro')
plt.plot(start[1::] - stop[:-1:], (stop - start)[1::], 'bo')
plt.show()