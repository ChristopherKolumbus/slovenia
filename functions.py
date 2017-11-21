import os, pickle
import numpy as np

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

def loadPickle(path):
    with open(path, 'rb') as fileObject:
        data = pickle.load(fileObject)
        fileObject.close()
    return data

def convertIndices2Times(timeAxis, indices):
    times = np.zeros(indices.shape)
    for i, index in enumerate(indices):
        times[i] = timeAxis[index]
    return times

def find_threshold_crossings(curve, threshold):
    up = []
    down = []
    n_minus_1 = 0
    for i, n in enumerate(curve):
        if n > threshold > n_minus_1:
            up.append(i)
        elif n_minus_1 > threshold > n:
            down.append(i)
        n_minus_1 = n
    return np.array(up), np.array(down)

def determine_threshold(envel):
    return np.nanmean(envel)

def calc_envelope(filtered, fs, low):
    envel = filtered ** 2
    envel = filter_signal(envel, fs, low)
    envel **= .5
    return envel


def find_nan_transitions(curve):
    start = []
    end = []
    n_minus_1 = 0
    for i, n in enumerate(curve):
        if np.isnan(n_minus_1) and not np.isnan(n):
            start.append(i)
        elif not np.isnan(n_minus_1) and np.isnan(n):
            end.append(i - 1)
        n_minus_1 = n
    if end[0] - start[0] < 0:
        del end[0]
    if end[-1] - start[-1] < 0:
        del start[-1]
    return np.array(start), np.array(end)


def calc_call_length(start, end):
    return np.abs(end - start)


def calc_area_under_curve(curve, start, end):
    area = np.zeros(start.shape)
    for i in range(start.size):
        area[i] = np.sum(curve[start[i]:end[i]])
    return area