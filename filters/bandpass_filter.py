"""
    This module will be used to bandpass the signal
"""
from scipy import signal # To use butter filter
import numpy as np
import config

def bandpass(data,state,bp):
    """
        Inputs:
            data {type:np.ndarray, shape:(config.CHUNK_SIZE)}
                - Input Data which needs to be filtered. Usually the sample size is 250.
                - This function will work with other chunk size different than config.CHUNK_SIZE

            states {type:list, len:6}
                - states record the information of the signal before this chunk.W

            bp {type:list, len:2}
                - This variable gives the start and stop frequencies to bandpass the signal.
                - The signal will be bandpass between bp[0] and bp[1].

        Outputs:
            bandpassOutput {type:np.ndarray, shape:(data.settings.CHUNK_SIZE)}
                - The input data bandpassed between bp[0] and bp[1]

            state {type:list, len:6}
                - The state of the current signal
        
        About this function:
            This function will apply bandpass filter to the input data.
    """
    start = bp[0]
    stop = bp[1]
    bp_Hz = np.zeros(0)
    bp_Hz = np.array([start,stop])
    b, a = signal.butter(3, bp_Hz/(config.SAMPLING_FREQUENCY / 2.0),'bandpass')
    bandpassOutput, state = signal.lfilter(b, a, data, zi=state)
    return bandpassOutput, state

def apply_bandpass_filter(data,start,stop,channels=list(range(8))):
    """
        Inputs:
            data {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size), ndim:3}
                - Input data that needs to filtered.
                - The data comes divided in epochs.
                - It is necessary for the input to have an ndim of 3 or else this function 
                will throw an exception

            start {type:int}
                - The starting frequeny to bandpass the signal
            
            stop {type:int}
                - The stopping frequeny to bandpass the signal

        Outputs:
            filteredData {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size)}
                - The data retaines its shape after being filtered.
            bp {type:list, len:2}
                - This variable gives the start and stop frequencies to bandpass the signal.
                - The signal will be bandpass between bp[0] and bp[1].

        About this function:
            This function applies bandpass filter to a batch of data all at once.
    """

    if(start == None):
        start = 1
    if(stop == None):
        stop = 50

    if (data.ndim != 3):
        raise Exception("""The ndim of the data needs to be 3. 
        Please make sure your data is in the format of (epochs,config.CHANNELS,chunk_size)""")
        pass
    
    filteredData = np.zeros(shape=data.shape)

    for c in channels:
        for e in range(data.shape[0]):
            filteredData[e,c], config.filter_states['bandpass'][c] = bandpass(data[e,c,:].reshape(-1),config.filter_states['bandpass'][c],[start,stop])
    
    return filteredData
