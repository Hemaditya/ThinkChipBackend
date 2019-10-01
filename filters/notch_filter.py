"""
    This is the code to apply notch filter on to the signal and also contains a bunch of supporter functions
"""
from scipy import signal # To use butter filter
import numpy as np

def notch_filter(data,states):
    """
        data {type:np.ndarray, shape:(chunk_size)}
            - Input Data which needs to be filtered. Usually the sample size is 250.

        states {type:list, len:6}
            - states record the information of the signal before this chunk.
        
        This function will apply notch filter to the input data.
    """
    # This is to remove the AC mains noise interference	of frequency of 50Hz(India)
    notch_freq_Hz = np.array([50.0])  # main + harmonic frequencies
    for freq_Hz in np.nditer(notch_freq_Hz):  # loop over each target freq
            bp_stop_Hz = freq_Hz + 3.0*np.array([-1, 1])  # set the stop band
            b, a = signal.butter(3, bp_stop_Hz/(250 / 2.0), 'bandstop')
            notchOutput, state = signal.lfilter(b, a, arr, zi=state)
            return notchOutput, state


def ApplyNotchFilter(data):
    """

    """
