'''
    The widget to measure user engagement
'''
import time
import os
import numpy as np
import threading
import filters as f
import pathlib
import pickle
import config
from widgets import Widget
# Make sure the global config file knows about this widget
import features as ft

# Game Class
class Game():
    """
        This will in general hold the media stats and settings of each of the media
    """

    def __init__(self,name,path):
        """
            Initialize game_name and path
        """
        self.game_name, self.game_path = name,path

    def save_data(self,data):
        """
            Just save the data to a location
        """
        import filters as f
        print({"CONSOLE: Filtering the data"})
        data = f.apply_dc_offset(data)
        data = f.apply_notch_filter(data)
        print(f"CONSOLE: Saving the data")
        with open(self.game_path/"filtered_data.pickle", 'wb+') as f:
            pickle.dump(data,f)

# ENG class
class ENG(Widget):
    """

    """

    # Init function
    def __init__(self,widget_name, widget_path, sessionName=None, offline=False):
        """
            Initialize a new widget object and create its path and other stuff
        """
        self.widget_name = widget_name
        self.widget_path = widget_path
        super().__init__(self.widget_name,self.widget_path)
        self.session_id, self.session_path = self.create_session()
        self.games = list(np.load("games.npy"))

        # Initialize the data reader for realtime data processing
        if(offline == False):
            self.data_reader = config.data_reader

        self.attention_matrix = []

        self.channel_mask = [0]

    def add_game(self,game_name):
        game_name = game_name.lower()
        if game_name in self.games:
            print(f"CONSOLE: the game {game_name} already exists")
            return 0
        self.games.append(game_name)
        print(f"CONSOLE: adding game {game_name} to games")
        np.save("games.npy",np.asarray(self.games))

    def remove_game(self,game_name):
        game_name = game_name.lower()
        games = list(np.load('games.npy'))
        if game_name not in games:
            print(f"CONSOLE: no game found with name {game_name}")
            return 0
        games.remove(game_name)

    def check_game_exists(self, game):
        if(game not in os.listdir(self.session_path)):
            print("CONSOLE: game {game_name} does not exists")
            return 0
            
        print("CONSOLE: game {game_name} not exists")
        return 1

    def create_game_session(self,game_name):
        """
            This function will create a folder for that game if it doesnot exist
        """

        # First check if the game exists or not
        game_path = self.session_path/pathlib.Path(game_name)
        print(f"CONSOLE:{self.session_id}")
        if not self.check_game_exists(game_name):
            print("CONSOLE: creating a folder for {game_name} in session {self.session_id}")
            os.mkdir(game_path)


        print("CONSOLE: the game {game_name} already exists in the session")
        return game_path

    def create_session(self,sessionName=None):
        """
            This function will create a new session Id for the user and create a folder for that session.
            All the data for this session will be stored in this folder
        """
        session_id = sessionName
        if(sessionName == None):
            session_id = time.strftime("%d%m%y_%H%M%S")
        print("CONSOLE: Create a new session {}".format(session_id))
        session_path = self.widget_path/session_id
        os.mkdir(session_path)
        return session_id, session_path

    def start_session(self,game_name="test", trails=20):
        """
            In this function, this widget is supposed to start reading data and keep saving it
            in its session folder every 10 seconds.
            This function is the command line version
        """
        # Check if the game exists if not, then create a new game
        game_path = self.session_path/pathlib.Path(game_name)
        if not self.check_game_exists(game_name):
            game_path = self.create_game_session(game_name)
            pass

        game_object = Game(game_name,game_path)
        data = np.zeros((1,config.CHUNK_SIZE,config.CHANNELS))
        for i in range(int(trails/10)):
            # Read 5 chunks at once and save the data
            data = np.vstack((data,self.data_reader.read_chunk(10)))
            x = threading.Thread(target=game_object.save_data,args=(data[1:],))
            x.start()

    def attention_per_channel(self, bandpower):
        """bandpower - numpy array of length 5"""
        # Do something to return attention given bandpower for
        # a single channel for a single epoch

        # temporary fix change this appropriately
        return np.mean(bandpower)

    def attention_overall(self, attention_per_channel):
        """attention_per_channel - np.array(num_of_channels)"""
        # Do something to generate
        # self.attention
        return np.mean(attention_per_channel)

    def test_start_session(self, game_name, channels=[0], read_length=10):
        """This function starts the widget and calls the functions to get data from cyton board
        using self.data_reader. Length of data section (temp_data) that is read at a single time
        is determined by read_length. This data section (temp_data) is passed to get_attention
        (in a different thread) which calculates the attention matrix for this data.
        channels: list of channels to use"""
        while True:
            temp_data = self.data_reader.read_chunk(read_length)

            # Thread because the below has too many loops
            # We don't have to drop data, as data will get dropped if
            # data_reader.read_chunk cannot be called for too long.
            t = threading.Thread(target=self.get_attention, args=(temp_data, channels,))
            t.start()

    def get_attention(self, temp_data, channel_mask=[0]):
        """This function gets the attention matrix from a section of data.
        length of this data section is determined by read_length.
        temp_data: np.array(epochs, channels, chunk_size)"""
        # Remove bad blocks
        #blocks_data = ft.remove_bad_epochs(temp_data, threshold=100,
                                           #channels=channel_mask, sliding_window=True)

        blocks_bandpower = ft.get_bandpower(temp_data, channel_mask)
        print(f"CONSOLE: bandpower Theta: {blocks_bandpower[1]}")
        #attention_per_channel = np.zeros((blocks_bandpower.shape[0], len(channel_mask)))
        #for idx, block in enumerate(blocks_bandpower):
        #    for channel in channel_mask:
        #        attention_per_channel[idx, channel] = self.attention_per_channel(block[channel])
        #    attention_per_epoch = self.attention_overall(attention_per_channel[idx])
        #    self.attention_matrix.append(attention_per_epoch)

        #    # For testing. Remove later
        #    print(f"CONSOLE: Attention per epoch: {attention_per_epoch}")


config.WIDGETS["ENG"] = {"class":ENG, "desc":"Unsterdant user engagement for different games"}
