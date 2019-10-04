from session import settings
import os


class Session():
    """
        This module is responsible for creating and deleting sessions
    """

    def __init__(self):
        """
            This function should initialize-
                SESSION_PATH: create the path for session if it doesnt already exist.W

        """
        self.SESSION_PATH = settings.SESSION_PATH
        pass

    def user_exists(self,username):
        """
            Check if the user with username exists. If true return 0, if user 
            does not exists return 1.
        """
        # Check if the user exists
        users = os.listdir(self.SESSION_PATH) 

        # If the user exists return 0
        if(username in users):
            return 0
        
        else:
            return 1
             
        pass



    def createUser(self,username):
        """
            Create a new session for user with username if it doesnot exist.
        """
        username = username.lower()
        user_path = self.SESSION_PATH/username
        os.mkdir(user_path)
        return user_path
         
        pass

