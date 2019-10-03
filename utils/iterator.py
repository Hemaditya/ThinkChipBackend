'''
    This module holds different iterators you can use to perform the sliding window on the data
'''

class Iterator():
    """
        Creates an iterator for your sliding window
    """
    def __init__(self,data,chunk_size=250,hop=125):
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

    def __iter__(self):
        """
            This funtion is called when an iterator is initialized.
        """
        self.idx = 0
        return self

    def __next__(self):
        # Check if you have reached the end of the data
        if(self.idx+self.chunk_size <= self.data.shape[0]):
            nextData = self.data[self.idx:(self.idx+self.chunk_size)]  
            self.idx = self.idx + self.hop
            return nextData
        else:
            raise StopIteration
