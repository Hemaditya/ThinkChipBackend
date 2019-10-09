import config
import filters
import threading
import numpy as np
import config

class EyeBlink():
    ''' Module to detect/read data for Eye Blinks '''

    def __init__(self,widget_path,trails=120):
        ''' Initialize stuff '''

    def save_data(self,data,f=0,verbose=False):
        ''' This function is called whenever you want to save the data '''
        """
            Inputs:
                data: np.ndarray
                - the data that you wanna save.
                f: int
                - 1 if you want to filter the data
                - 0 if you want to save raw data
        """
        flag = '[r]'
        if(f == 1):
            flag = '[f]'
            if verbose:
                print(f"CONSOLE: Filtering the data")
            data = filters.apply_dc_offset(data)
            data = filters.apply_notch_filter(data)

        self.data_buffer = np.vstack((self.data_buffer,data))
        file_name = flag+game+_self.t+".pickle"
        file_path = self.path/file_name
        if verbose:
            print(f"CONSOLE: Saving data")
        with open(file_path,'wb+') as f:
            pickle.dump(self.data_buffer[1:],f)
    
    def detect_blinks(self,data, channels=[0]):
        ''' Detect eye blinks here '''
        data = filters.apply_dc_offset(data)
        data = filters.apply_notch_filter(data)
        data = filters.apply_bandpass_filter(data,1,10)
        data = data[:,channels,:].reshape(-1)

        if(data.max() <= 200.0 and data.max() >= 100.0):
            print("Blink Detected")
        else:
            print("No Blink Detected")
        

    def run_real_time(self):
        while True:
            data = config.data_reader.read_chunk(n_chunks=1)
            t = threading.Thread(target=self.detect_blinks,args=(data,))
            t.start()


