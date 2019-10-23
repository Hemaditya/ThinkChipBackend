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

def load_all_pickle_files(path,vstack=False):
    # This function will load the data from all the pickle files in the given path variable
    # If vstack is true, then it will combine data of all files into a single numpy array
    # by stacking them one upon other
    path = Path(path)
    if (os.path.exists(path)):
        print(f"Loading data from {path} ")
        pass
    else:
        print(f"The path: {path} does not exist")
        return 

    data = []
    for file in os.listdir(path):
        if 'pickle' in file:
            print(f"Loading File: {file}")
            with open(path/file,'rb') as f_:
                d = pickle.load(f_)
                data.append(d)
       
    if(vstack == True):
        print(f"Using vstack=True")
        data = np.vstack(data)
    else:
        data = np.array(data)
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
        
