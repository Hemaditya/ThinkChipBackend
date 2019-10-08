"""
    This module is for ENG widget, command line version
"""
import filters
import time
import config
import pickle
import numpy as np
import threading

class ENG():
    ''' The base class for ENG module '''

    def __init__(self,widget_path,trails=120):
        ''' Each of the widgets will be initialized with a path to their widget '''

        self.path = widget_path
        self.data_buffer = np.zeros(shape=(1,config.CHANNELS,config.CHUNK_SIZE))
        self.t = time.strftime("%d%m%y_%H%M%S")
        # This is the defult and can be reset
        self.trails = trails
        self.games = np.load(config.ROOT_DIR/'widgets/games.npy')

    def save_data(self,data,game,f=0,verbose=False):
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
        file_name = flag+game+self.t+".pickle"
        file_path = self.path/file_name
        if verbose:
            print(f"CONSOLE: Saving data")
        with open(file_path,'wb+') as f:
            pickle.dump(self.data_buffer[1:],f)

    def run(self):
        ''' This function will be called whenever you want to start the widget '''

        # First reset the states variables
        config.reset_filter_states()
        
        x = 0
        while x != 'q':
            for i,g in enumerate(self.games):
                print(i+1,".",g)
            print("Press q to exit ")
            x = input("Enter the game you wanna play: ")
            if x != 'q':
                x = int(x) - 1 
                if(x < 0 or x >= self.games.shape[0]):
                    print(f"CONSOLE: Enter proper varible") 
                    continue
                self.t = time.strftime("%d%m%y_%H%M%S")
                for i in range(int(self.trails/5)):
                    print(f"CONSOLE: {int(self.trails/5)-i} trails left")
                    data = config.data_reader.read_chunk(5)
                    t = threading.Thread(target=self.save_data, args=(data,self.games[x],1))
                    t.start()
