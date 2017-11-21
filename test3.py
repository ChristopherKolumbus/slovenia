import pickle
import numpy as np
import functions
from matplotlib import pyplot as plt
import pickle

import numpy as np
from matplotlib import pyplot as plt

import functions


def loadPickle(path):
    with open(path, 'rb') as pickleObject:
        data = pickle.load(pickleObject)
        pickleObject.close()
    return data

path = r'C:\Users\chris\Documents\results_2016_0853'
pickleList = functions.findFiles(path, '.p')
data = loadPickle(pickleList[0])
callStart = data['CallStart']
callEnd = data['CallEnd']
print(callStart)
print(callEnd)
plt.hist(callEnd-callStart,bins=50)
plt.show()
plt.hist(np.diff(callStart),bins=50)
plt.show()