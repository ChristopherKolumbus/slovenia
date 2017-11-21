import numpy as np

from scipy import signal
from matplotlib import pyplot as plt

from thunderfish import dataloader as dl


def raw_load(data_path, window):
    with dl.open_data(data_path) as data:
        fs = data.samplerate
        raw = data[round(window[0] * fs):round(window[1] * fs)]
        data.close()
        return fs, raw


def filter_signal(raw, fs, low=0, high=None):
    nyq = fs / 2
    if high is None:
        b, a = signal.butter(2, [low / nyq], btype='lowpass')
    else:
        b, a = signal.butter(2, [low / nyq, high / nyq], btype='bandpass')
    filtered = signal.filtfilt(b, a, raw)
    return filtered


def calc_envelope(filtered, fs, low):
    envel = filtered ** 2
    envel = filter_signal(envel, fs, low)
    envel **= .5
    envel = np.nan_to_num(envel)
    return envel


def find_threshold_crossings(curve, threshold, min_up_duration, min_down_duration):
    n_minus_1 = 0
    up = []
    down = []
    up_flag = 0
    down_flag = 1
    up_count = 0
    down_count = 0
    for i, n in enumerate(curve):
        if n_minus_1 < threshold < n and up_flag == 0 and down_count == 0:
            up.append(i)
            up_flag = 1
            down_flag = 0
            up_count = min_up_duration
        elif n_minus_1 > threshold > n and down_flag == 0 and up_count == 0:
            down.append(i)
            up_flag = 0
            down_flag = 1
            down_count = min_down_duration
        n_minus_1 = n
        if up_count > 0:
            up_count -= 1
        elif down_count > 0:
            down_count -= 1
    if len(up) > len(down):
        del up[-1]

    return np.array(up), np.array(down)


def find_calls(curve, start, stop, threshold):
    area = np.zeros(start.shape)
    std = np.zeros(start.shape)
    for i, n in enumerate(zip(start, stop)):
        area[i] = np.sum(curve[n[0]:n[1]]) / curve[n[0]:n[1]].size
        std[i] = np.std(curve[n[0]:n[1]])
    area = (area-np.min(area)) / (np.max(area)-np.min(area))
    std = (std-np.min(std)) / (np.max(std)-np.min(std))
    score = area - std
    score = (score-np.min(score)) / (np.max(score)-np.min(score))
    #delete = []
    #for i, n in enumerate(score):
    #    if n < threshold:
    #        delete.append(i)
    #score = np.delete(score, delete)
    #start = np.delete(start, delete)
    #stop = np.delete(stop, delete)
    #area = np.delete(area, delete)
    #std = np.delete(std, delete)
    return start, stop, area, std, score


raw_path = r'C:\Users\chris\Documents\plittoralis-timestamps\recordings\2015-07-29-aa\trace-6.raw'
time_window = (0, -1)
low_bandpass = 6000
high_bandpass = 10000
low_lowpass = 5
envelope_threshold = 0.15
score_threshold = .2
Fs, raw_signal = raw_load(raw_path, time_window)
min_call_length = round(.5 * 1000)
min_inter_call = round(.1 * 1000)
filtered_signal = filter_signal(raw_signal, Fs, low_bandpass, high_bandpass)
signal_envelope = calc_envelope(filtered_signal, Fs, low_lowpass)
signal_envelope = signal_envelope[::round(Fs / 1000)]
signal_envelope = (signal_envelope - np.min(signal_envelope)) / (np.max(signal_envelope) - np.min(signal_envelope))
call_start, call_end = find_threshold_crossings(signal_envelope, envelope_threshold, min_call_length, min_inter_call)
call_start, call_end, call_area, call_std, call_score = find_calls(signal_envelope, call_start, call_end, score_threshold)


t = np.arange(0, len(signal_envelope)) * 1/1000
#fig, ax = plt.subplots(2, sharex=True)
plt.plot(t, signal_envelope)
plt.plot(t[call_start], signal_envelope[call_start], 'go')
plt.plot(t[call_end], signal_envelope[call_end], 'ro')
plt.plot(t[np.round(call_start + (call_end - call_start)/2).astype(int)], call_area, 'co')
plt.plot(t[np.round(call_start + (call_end - call_start)/2).astype(int)], call_std, 'yo')
plt.plot(t[np.round(call_start + (call_end - call_start)/2).astype(int)], call_score, 'bo')
#ax[0].plot(t[np.round(call_start + (call_end - call_start)/2).astype(int)], call_score, 'yo')
#ax[1].plot(t, filtered_signal)
#ax[1].plot(t[call_start], np.zeros(call_start.shape), 'go')
#ax[1].plot(t[call_end], np.zeros(call_end.shape), 'ro')
plt.show()