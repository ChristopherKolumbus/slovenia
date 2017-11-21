import os
import pickle

import numpy as np

import functions


def loadPickle(path):
    with open(path, 'rb') as pickleObject:
        data = pickle.load(pickleObject)
        pickleObject.close()
    return data

def convertIndices2Times(timeAxis, indices):
    times = np.zeros(indices.shape)
    for i, index in enumerate(indices):
        times[i] = timeAxis[index]
    return times

path = r'C:\Users\chris\Documents\results_2016_0853'
pickleFileList = functions.findFiles(path, '.p')
for file in pickleFileList:
    dataInput = loadPickle(file)
    callStart = convertIndices2Times(dataInput['Time'], dataInput['CallStart'])
    callEnd = convertIndices2Times(dataInput['Time'], dataInput['CallEnd'])
    dataOutput = {'CallStart': callStart, 'CallEnd': callEnd}
    root, ext = os.path.splitext(file)
    with open(root + 'T' + ext, 'wb') as outputFile:
        pickle.dump(dataOutput, outputFile)
        outputFile.close()
