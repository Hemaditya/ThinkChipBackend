"""
    This module is responsible for detecting eye_blinks in the data.
"""
import numpy as np
import config

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

def get_eye_blinks(data,threshold=None, channels=[0],sliding_window=True):
    """
        Inputs:
            data:{type:np.ndarray, shape:(epochs,config.CHANNELS,config.CHUNK_SIZE)}

        Outputs:
            energy:{type:float}

        About this function:
            This function finds the energy per epoch.
    """

    data = data.transpose(1,0,2)
    data = data.reshape(data.shape[0],-1)

    if(sliding_window == True):
        dataIterator = utils.sliding_window(data)
