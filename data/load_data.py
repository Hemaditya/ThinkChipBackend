"""
    This module will load offline data to process it.
    This module works only for ENG widgets
"""
import os
import sys
import pickle
import pathlib
import config
import session
import numpy as np

def load_data(username):
    ''' Load data of the user username '''
    '''
        Inputs:
            username: string
                - The username of the person who's data you want to load.

        Outputs:
            data: dictionary
                - Keys are the widget names and values are the contents of the widget

    '''
    path = config.SESSION_DIR
    username = username.lower()
    path = path/username
    if not os.path.isdir(username):
        print(f"CONSOLE: The username: {username} does not exist")
        return 0

    widgtes = os.listdir(path) 
    data = {}
    for w in widgets:
        data[w] = {}
        w_path = path/w
        for u in os.listdir(w_path):
            with open(w_path/u,'rb') as f:
                data[w][u] = pickle.load(f)

    return data

def load_widget_data(user, widget):
    ''' This function adds a new widget to the user '''

    """
        user: str or Path object
        - if user is a string, it is assumed to be username.
        - if user is a Path object, it is assumed to be the path to the user's directory

        Outputs:
        - Widget data dictionary
        - for each of the game, a dictionary will be created with timestamp as its key and
            the values will be its data.
    """

    widget_path = session.check_widget(user,widget)

    if widget_path == 0:
        print(f"CONSOLE: Cannot load the data for {widget} as it does not exist")
        return 0

    if os.listdir(widget_path) == 0:
        print(f"CONSOLE: There is no data present in {widget}") 
        return 0

    games = np.load('../widgets/games.npy')

    widget_data = {}
    for g in games:
        widget_data[g] = {}

    #  Start loding the contents in the wiget_path
    game_files = os.listdir(widget_path)

    for g in game_files:
        # First Extract the game name
        game_name = g.split('|')[0][3:]
        # Get the timestamp of that sample
        timestamp = g.split('|')[1].split('.')[0] 
        
        # Get the numpy data
        game_f = open(widget_path/g,'rb')
        game_data = pickle.load(game_f)

        # Put data in in the dictionary
        widget_data[game_name][timestamp] = game_data

    return widget_data

