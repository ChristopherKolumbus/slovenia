import os
import pickle
import shelve

data_path = r'C:\Users\chris\Documents\calltiming_17_11_21'

data = shelve.open(os.path.join(data_path, 'data'))
for ind, item in enumerate(os.listdir(data_path)):
    if item.endswith('.p'):
        with open(os.path.join(data_path, item), 'rb') as f:
            data[str(ind) + '. trace'] = pickle.load(f)
data.close()