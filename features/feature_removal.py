"""
    This module is responsible for detecting eye_blinks in the data.
"""
import numpy as np
import config
from utils import Iterator

def energy_of_epoch(data):
    """
        Inputs:
            data:{type:np.ndarray, shape:(config.CHUNK_SIZE)}

        Outputs:
            energy:{type:float}

        About this function:
            This function finds the energy per epoch.
    """
    
    energy = np.square(data)
    energy = np.mean(energy)
    return energy

def remove_bad_epochs(data,threshold=None, channels=[0],sliding_window=True):
    """
        Inputs:
            data:{type:np.ndarray, shape:(epochs,config.CHANNELS,config.CHUNK_SIZE)}
            threshold:{type:int}
                - The threshold to test for bad epoch against 
            channels:{type:list}
                - The channels to test this on
            sliding_window:{type:boolean}
                - If you want to use a sliding_window or not

        Outputs:
            data:{type:np.ndarray}
                - Data after removing bad epochs

        About this function:
            This function finds the energy per epoch.
    """
    oldData = np.copy(data)
    data = data.transpose(1,0,2)
    data = data.reshape(data.shape[0],-1)

    dataIterator = []
    for c in channels:
        if(sliding_window == True):
            dataIterator.append(utils.Iterator(data[c]))
        else:
            dataIterator.append(data[c])

    bad_epochs = [] 
    for c in channels:
        for D in dataIterator[c]:
            for i,d in enumerate(D):
                if(energy_of_epoch(d) >= threshold):
                    bad_epochs.append(i)
               
    
    # Remove duplicate epochs
    bad_epochs = np.array(list(set(bad_epochs)))
    if(sliding_window == True):
        # Generate indices for bad_epochs in oldData
        bad_epochs = bad_epochs*dataIterator[0].hop 
        bad_epochs = np.floor(bad_epochs/dataIterator[0].chunk_size)
    data = np.delete(oldData,bad_epochs,axis=0)
        
    return data
