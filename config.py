"""
    These are the default settings that will be used by all modules.
    U can import global variables from this module and use them.
    modules are also allowed to change the default settings
"""
import os
import pathlib
from pathlib import Path


# Create this as the root directory and add it to your path
ROOT_DIR = pathlib.Path(os.path.dirname(__file__))
# The directory where session data will be stored
# The path to the APP
APP_PATH = Path(os.environ['HOME'])/'.config'/'ThinkChip'

'Session data will be stored in the path SESSION_PATH'
SESSION_PATH = APP_PATH/'SessionData'
# CHUNK_SIZE defines the size of each epoch in the data
CHUNK_SIZE = 250

# SAMPLING_FREQUENCY is device specific and needs to be changed for every device
SAMPLING_FREQUENCY = 250

# CHANNELS  variable is also device specific
CHANNELS = 8

# threshold class will hold thresholds for all the different artifacts
class threshold():
    '''
        This module is a place to hold different thresholds
    '''

    def __init__(self):

        EYE_BLINK = 100 # After signal is bandpassed between 1,10

THRESHOLD = threshold()

"""
    These will be set of widgets that are available for user to test out
"""
WIDGETS = {}

""" This file will hold the reader or streamer for the data"""
try:
    from core.app import OpenBCI
    data_reader = OpenBCI(chunk_size=CHUNK_SIZE)
    print('Using OpenBCI')
except:
    from core.random_gen import dataReader
    print('Using config.dataReader - random number')
    data_reader = dataReader()

# These are the settings for filters
filter_states = {}
def reset_filter_states():
    global filter_states
    filter_states['dc'] = {}
    filter_states['notch'] = {}
    filter_states['bandpass'] = {}
    for i in range(CHANNELS):
        filter_states['dc'][i] = [0,0]
        filter_states['notch'][i] = [0,0,0,0,0,0]
        filter_states['bandpass'][i] = [0,0,0,0,0,0]
