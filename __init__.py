import os
import sys
import config

# sys.path is responsible will help see whether this python module is importable or not
sys.path.append(os.path.dirname(__file__))
# set the root directory
config.ROOT_DIR = os.path.dirname(__file__)
