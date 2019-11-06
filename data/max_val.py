import numpy as np
def max_val(data_in, threshold=400):
    """
        data: Should be of the shape:(epochs, channels, chunk_size)
        threshold: max_threshold to be allowed in that epoch
    """
    
    indxs = np.unique(np.where(np.abs(data_in[...,:]) > threshold)[0])
    return np.delete(data_in, indxs, axis=0)
