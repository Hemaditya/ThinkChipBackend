import numpy as np
import time
class dataReader():

    def __init__(self):
        pass

    def read_chunk(self, n_chunks):
        for i in range(n_chunks):
            print(i)
            time.sleep(1)
        x = np.random.randn(10,8,250)
        return x
