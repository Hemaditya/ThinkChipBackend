"""
        This module is responsible for detecting eye_blinks in the data.
"""
import numpy as np
import filters
import config
import sys
import utils
from utils import Iterator

def energy_of_epoch(data,verbose=False):
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
        if(verbose == True):
            print(f"CONSOLE: ENEGERGY: {energy}")
        return energy

def remove_bad_epochs(data, thresh_fn, threshold=100, channels=[0], sliding_window=True):
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
        data = filters.apply_bandpass_filter(data,1,10)
        data = data.transpose(1,0,2)
        data = data.reshape(data.shape[0],-1)

        # Puts each channel as a numpy array in the list
        dataIterator = []
        for c in channels:
                if(sliding_window == True):
                        dataIterator.append(utils.iterator.getIterator(data[c]))
                else:
                        dataIterator.append(data[c])
        dataIterator = np.asarray(dataIterator)

        # Iterate over each block in each channel and find bad blocks
        # corresponding to blinks as blocks with energy above the threshold.
        bad_epochs = []
        for i,c in enumerate(channels):
                for index, block in enumerate(dataIterator[i]):
                        if(thresh_fn(block) >= threshold):
                                bad_epochs.append(index)

        # Reshape it back to epochs,channels,chunk_size
        # so that epochs are in 0th axis to remove bad epochs.
        dataIterator = dataIterator.transpose(1,0,2)
        # Remove duplicate epochs
        bad_epochs = np.array(list(set(bad_epochs)))
        #print(bad_epochs)
        # Now delete these bad epochs
        data = np.delete(dataIterator, bad_epochs, axis=0)
        #print(f"CONSOLE: deleted bad epochs, new data shape: {data.shape}")

        return data

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
