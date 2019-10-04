"""
    This is module which holds global settings for session that are created
"""

"""
    This value is the number of epochs for current session and will be updated when creating a new session.
    EPOCHS variable will only be used while recording the data and/or doing real time analysis and not while 
    postprocessing.
"""
EPOCHS = 0

"""
    Setting Path variables
"""
'The path to this Application settings is APP_PATH'
import os
from pathlib import Path
APP_PATH = Path(os.environ['HOME'])/'.config'
'Session data will be stored in the path SESSION_PATH'
SESSION_PATH = APP_PATH/'SessionData'
if(os.path.exists(SESSION_PATH) == False):
    ' If the path to session data does not exist, the create it'
    os.mkdir(SESSION_PATH)

