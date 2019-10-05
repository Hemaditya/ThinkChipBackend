"""
    These are the default settings that will be used by all modules.
    U can import global variables from this module and use them.
    modules are also allowed to change the default settings
"""
import os


# Create this as the root directory and add it to your path
ROOT_DIR = os.path.dirname(__file__)

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
data_reader = None
