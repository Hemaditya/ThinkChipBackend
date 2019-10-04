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
APP_PATH = Path(os.environ['HOME'])/'.config'/'ThinkChip'
if(not os.path.exists(APP_PATH)):
    print(f"CONSOLE: the App path does not exist")
    print(f"CONSOLE: Creating App path at {APP_PATH}")
    os.mkdir(APP_PATH)

'Session data will be stored in the path SESSION_PATH'
SESSION_PATH = APP_PATH/'SessionData'
if(os.path.exists(SESSION_PATH) == False):
    ' If the path to session data does not exist, the create it'
    print(f"CONSOLE: The Session path does not exist")
    print(f"CONSOLE: Creating Session path at {SESSION_PATH}")
    os.mkdir(SESSION_PATH)

