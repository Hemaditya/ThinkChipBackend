"""
    This is the code to apply notch filter on to the signal and also contains a bunch of supporter functions
"""
from scipy import signal # To use butter filter
import numpy as np
import config

def notch_filter(data,states):
    """
        Inputs:
            data {type:np.ndarray, shape:(config.CHUNK_SIZE)}
                - Input Data which needs to be filtered. Usually the sample size is 250.
                - This function will work with other chunk size different than config.CHUNK_SIZE

            states {type:list, len:6}
                - states record the information of the signal before this chunk.

        Outputs:
            notchOutput {type:np.ndarray, shape:(data.settings.CHUNK_SIZE)}
                - The input data notched at 50.0Hz

            state {type:list, len:6}
                - The state of the current signal
        
        About this function:
            This function will apply notch filter to the input data.
    """
    # This is to remove the AC mains noise interference	of frequency of 50Hz(India)
    notch_freq_Hz = np.array([50.0])  # main + harmonic frequencies
    for freq_Hz in np.nditer(notch_freq_Hz):  # loop over each target freq
            bp_stop_Hz = freq_Hz + 3.0*np.array([-1, 1])  # set the stop band
            b, a = signal.butter(3, bp_stop_Hz/(config.SAMPLING_FREQUENCY / 2.0), 'bandstop')
            notchOutput, state = signal.lfilter(b, a, data, zi=states)
            return notchOutput, state



def apply_notch_filter(data):
    """
        Inputs:
            data {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size), ndim:3}
                - Input data that needs to filtered.
                - The data comes divided in epochs.
                - It is necessary for the input to have an ndim of 3 or else this function 
                will throw an exception

        Outputs:
            filteredData {type:np.ndarray, shape:(epochs,config.CHANNELS,chunk_size)}
                - The data retaines its shape after being filtered.

        About this function:
            This function applies notch filter to a batch of data all at once.
    """

    if (data.ndim != 3):
        raise Exception("""The ndim of the data needs to be 3. 
        Please make sure your data is in the format of (epochs,config.CHANNELS,chunk_size)""")
        pass
    
    filteredData = np.zeros(shape=data.shape)

    for c in range(data.shape[1]):
        state = [0,0,0,0,0,0]
        for e in range(data.shape[0]):
            filteredData[e,c], state = notch_filter(data[e,c,:].reshape(-1),state)
    
    return filteredData
