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
