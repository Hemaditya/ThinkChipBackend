import numpy as np
import time

class dataReader():

    def __init__(self, verbose=False):
        self.verbose = verbose
        pass

    def read_chunk(self, n_chunks):
        for i in range(n_chunks):
            if(self.verbose):
                print(i)
            time.sleep(1)
        x = np.random.randn(n_chunks,8,250)
        return x
