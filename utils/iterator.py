'''
    This module holds different iterators you can use to perform the sliding window on the data
'''
import numpy as np

class Iterator():
    """
        Creates an iterator for your sliding window
    """
    def __init__(self, data, chunk_size=250, hop=125, window=True):
        """
            Inputs:
                data:{type:np.ndarray, shape=(epochs*chunk_size)}
                    - Input Data
                chunk_size:{type:int}
                    - the amount of samples from the start of the hop
                hop:{type:int}
                    - the amount jump in the indices
        """

        self.data = data
        self.chunk_size = chunk_size
        self.hop = hop
        if window:
            self.window = np.hanning(chunk_size)

    def __iter__(self):
        """
            This funtion is called when an iterator is initialized.
        """
        self.idx = 0
        return self

    def __next__(self):
        # Check if you have reached the end of the data
        if self.idx+self.chunk_size <= self.data.shape[0]:

            nextData = self.data[self.idx:(self.idx+self.chunk_size)]

            try:
                nextData = nextData*self.window
            except AttributeError:
                pass

            self.idx = self.idx + self.hop
            return nextData

        raise StopIteration


def getIterator(data, chunk_size=250,hop=125,window=True):
    """
        This function takes a data with shape(epochs, channels, chunk_size) and
        returns a new data with how it should iterate.W

        output:
            data with epochs which the iterator has gives out.
    """
    iterator = Iterator(data,chunk_size,hop,window)
    data = []
    for i in iterator:
        data.append(i)

    data = np.asarray(data)
    return data
