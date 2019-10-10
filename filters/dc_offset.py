"""
    This module applies DC offset to the data
"""
from scipy import signal
import numpy as np
import config

def dc_offset(data,state):
    """
        Inputs:
            data {type:np.ndarray, shape:(config.CHUNK_SIZE)}
                - Input Data which needs to be dc_offset. Usually the sample size is 250.
                - This function will work with other chunk size different than config.CHUNK_SIZE

            states {type:list, len:2}
                - states record the information of the signal before this chunk.

        Outputs:
            dcOffsetOut {type:np.ndarray, shape:(data.settings.CHUNK_SIZE)}
                - The input data dc offsetted

            state {type:list, len:2}
                - The state of the current signal
        
        About this function:
            This function will remove dc offset filter to the input data.
    """
    hp_cutoff_Hz = 1.0 # cuttoff freq of 1 Hz (from 0-1Hz all the freqs at attenuated)
    b, a = signal.butter(2, hp_cutoff_Hz/(config.SAMPLING_FREQUENCY / 2.0), 'highpass')
    dcOffsetOut, state = signal.lfilter(b, a, data, zi=state)
    return dcOffsetOut, state

def apply_dc_offset(data):
    """
        Inputs:
            data {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size), ndim:3}
                - Input data that needs to dc offset.
                - The data comes divided in epochs.
                - It is necessary for the input to have an ndim of 3 or else this function 
                will throw an exception

        Outputs:
            offsetData {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size)}
                - The data retaines its shape after being dc offsetted.

        About this function:
            This function applies dc offset to a batch of data all at once.
    """
    if (data.ndim != 3):
        raise Exception("""The ndim of the data needs to be 3. 
        Please make sure your data is in the format of (epochs,config.CHANNELS,chunk_size)""")
        pass
    
    offsetData = np.zeros(shape=data.shape)

    for c in range(data.shape[1]):
        for e in range(data.shape[0]):
            offsetData[e,c], config.filter_states['dc'][c] = dc_offset(data[e,c,:].reshape(-1),config.filter_states['dc'][c])
    
    return offsetData

