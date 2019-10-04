'''
    The widget to measure user engagement
'''
from widgets import *
import time
import numpy as np
import threading
import filters as f
import pickle
import config

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
        print({"CONSOLE: Filtering the data"})
        data = f.apply_dc_offset(data)
        data = f.apply_notch_filter(data)
        with open(self.game_path/"filtered_data.pickle", 'wb') as f:
            pickle.dump(data,f)

class ENG(Widget):
    """
        
    """

    def __init__(self,widget_name, widget_path, sessionName=None, offline=False):
        """
            Initialize a new widget object and create its path and other stuff
        """
        super().__init__(self.widget_name,self.widget_path) 
        self.session_id, self.session_path = self.create_session(sessionName)
        self.games = list(np.load("games.npy"))

        # Initialize the data reader for realtime data processing 
        if(offline == False):
            self.data_reader = config.data_reader

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
            return 0
        
        return 1

    def create_game_session(self,game_name):
        """
            This function will create a folder for that game if it doesnot exist
        """

        # First check if the game exists or not
        if not check_game_exists(game_name):
            print("CONSOLE: creating a folder for {game_name} in session {self.session_id}") 
        game_path = self.session_id/game_name
        return game_path

    def create_session(self,sessionName=None):
        """
            This function will create a new session Id for the user and create a folder for that session.
            All the data for this session will be stored in this folder
        """
        session_id = sessionName
        if(sessioName == None):
            session_id = time.strftime("%d%m%y_%H%M%S")
        
        print("CONSOLE: Create a new session {}".format(session_id))
        session_path = self.widget_path/session_id
        os.mkdir(session_path)
        return session_id, session_path

    def start_session(self,game_name, trails=120):
        """
            In this function, this widget is supposed to start reading data and keep saving it
            in its session folder every 10 seconds.

            This function is the command line version
        """
        # Check if the game exists if not, then create a new game
        game_path = self.session_path/game_name
        if not check_game_exists(game_name):
            game_path = self.create_game_session(game_name)
        
        game_object = Game(game_name,game_path)
        
        for i in range(int(trails/5)):
            # Read 5 chunks at once and save the data
            data = self.data_reader.read_chunk(5)
            x = threading.Thread(target=game_object.save_data,args=(data,))
            x.start()

