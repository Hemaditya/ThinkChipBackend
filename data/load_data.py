"""
    This module will load offline data to process it.
"""
import os
import sys
import pickle
from pathlib import Path
import config
import numpy as np
import matplotlib.pyplot as plt
from features import remove_bad_epochs
from features import energy_of_epoch

def load_all_pickle_files(path,vstack=False,remove_first=10):
    # This function will load the data from all the pickle files in the given path variable
    # If vstack is true, then it will combine data of all files into a single numpy array
    # by stacking them one upon other
    # Remove first specifies the number of epoch you want to ignore at the beginning
    path = Path(path)
    if (os.path.exists(path)):
        print(f"Loading data from {path} ")
        pass
    else:
        print(f"The path: {path} does not exist")
        return 

    data = []
    if(remove_first != 0):
        print(f"First {remove_first} epochs will be removed while loading the data.")
    for file in os.listdir(path):
        if 'pickle' in file:
            print(f"Loading File: {file}")
            with open(path/file,'rb') as f_:
                d = pickle.load(f_)
                data.append(d[remove_first:])
       
    if(vstack == True):
        print(f"Using vstack=True")
        data = np.vstack(data)
    else:
        #data = np.array(data)
        pass
    return data

def plot_signal(data,channels=[0]):
    """ This function will plot the signal """

    w,h = len(channels)*7, len(channels)*8
    fig = plt.figure(figsize=(w,h))

    nrows = len(channels)//2 + 1
    ncols = 2
    
    for i,c in enumerate(channels):
        ax = fig.add_subplot(nrows,ncols,i+1)
        ax.plot(data[:,c,:].reshape(-1))
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitube")
        ax.set_title(f"Channel: {c}")
        
def clean_data(*args, channels=[0], threshold=400):
    ''' This funtion will clean up the data and remove bad epochs based on the threshold'''
    ''' Each numpy array passed as an argument is treated as a seperate data file and then processed'''
    
    clean_data = []
    
    for i, data_file in enumerate(args):
        print(f"Processing file:{i+1}")
        config.reset_filter_states()
        clean_data.append(remove_bad_epochs(data_file,energy_of_epoch,channels=channels,threshold=threshold))
        
    if(len(clean_data) == 1):
        return clean_data[0]
    else:
        return clean_data

def epoch_bandpower(*args,per_epoch=1,channels=[0],relative=False):
    ''' You can give as many files as you want an this function will find the 
        bandpower for each of them and return them as a list '''
    ''' If relative is True, then bandpower percentage for each band will be calculated'''
    ''' Per epochs refers to how many epochs together will be used to find bandpower.'''
    
    _bandpower = []
    for j, data in enumerate(args):
        config.reset_filter_states()
        print(f"Processing file:{j+1}")
        idxs = list(range(0,data.shape[0],per_epoch))
        _b = []
        for i in idxs:
            _b.append(get_bandpower(data[i:i+per_epoch],relative=relative,channels=channels))
        _bandpower.append(np.array(_b))
    
    if(len(_bandpower) == 1):
        return _bandpower[0]
    else:
        return _bandpower

def plot_bandpower(data,bands=['delta','theta','alpha','beta']):
    ''' Plot the badpower of a given data'''
    ''' Expected Input: (epochs, channels, bands)'''
    
    w, h = len(bands)//2*7, (len(bands)//2)*8
    fig = plt.figure(figsize=(w,h))
    nrows = len(bands)//2 + 1 # // is the same as divide and do math.floor
    ncols = 2
    
    data = data.transpose(1,0,2)
    for i, b in enumerate(data):
        ax = fig.add_subplot(nrows,ncols,i+1)
        for j, band_ in enumerate(bands):
            ax.plot(b[:,j].reshape(-1), alpha=0.6, label=bands[j])
            ax.set_title(f"Channel {i+1}")
            ax.set_xlabel('Epoch')
            ax.set_ylabel('bandpower')
            ax.legend()
