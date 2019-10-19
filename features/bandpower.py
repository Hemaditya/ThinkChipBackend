import numpy as np
# Example: plot the 0.5 - 2 Hz band
def bandpower(data, sf, band, window_sec=None, relative=False):
    """Compute the average power of the signal x in a specific frequency band.

    Inputs
    ----------
    data : 1d-array
        Input signal in the time-domain.
    sf : float
        Sampling frequency of the data.
    band : list
        Lower and upper frequencies of the band of interest.
    window_sec : float
        Length of each window in seconds.
        If None, window_sec = (1 / min(band)) * 2
    relative : boolean
        If True, return the relative power (= divided by the total power of the signal).
        If False (default), return the absolute power.

    Return
    ------
    bp : float
        Absolute or relative band power.
    """
    from scipy.signal import welch
    from scipy.integrate import simps
    import numpy as np
    band = np.asarray(band)
    low, high = band

    # Define window length
    if window_sec is not None:
        nperseg = window_sec * sf
    else:
        nperseg = (2 / low) * sf

    # Compute the modified periodogram (Welch)
    freqs, psd = welch(data, sf, nperseg=nperseg)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Find closest indices of band in frequency vector
    idx_band = np.logical_and(freqs >= low, freqs <= high)

    # Integral approximation of the spectrum using Simpson's rule.
    bp = simps(psd[idx_band], dx=freq_res)

    if relative:
        bp /= simps(psd, dx=freq_res)
    return bp

def get_bandpower(data, channels=[0], relative=False):
    """
       About this function:
            - Gets the bandpower of a signal and seperates each bands into 5 categories:
            - delta(0.2-4Hz)
            - theta(4-8Hz)
            - alpha(8-13Hz)
            - beta(15-30Hz)
            - gamma(30-50Hz)

        Inputs:
            data:{type:np.ndarray, shape:(epochs,channels,chunk_size)}
                - Input time signal data
            channels {type:list}
                - All the channels for which you want the bandpower.

        Outputs:
            bandPower {type:np.ndarray,shape:(channels,5)}
                - Bandpower of all the channels for all the epochs

    """
    oldData = np.copy(data)

    # create band limtis
    band = {}
    band['delta'] = [1,4]
    band['theta'] = [4,8]
    band['alpha'] = [8,14]
    band['beta'] = [16,30]
    band['gamma'] = [30,50]

    data = data.transpose(1,0,2)
    data = data[channels]
    data = data.reshape(data.shape[0],-1)
    chanD = []
    for i,c in enumerate(data):
            bandP = []
            for k in band:
                    bp = bandpower(c,250.0,band[k],2,relative=relative)
                    bandP.append(bp)
            chanD.append(bandP)

    bandPower = np.asarray(chanD)
    return bandPower
