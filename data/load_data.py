"""
    This module will load offline data to process it.
"""
import os
import sys
import pickle
import pathlib
import config

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
    path = pathlib.Path(config.SESSION_DIR)
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


