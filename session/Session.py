from session import settings
import shutil
from session import User
import config
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

    def user_exists(self,user_name):
        """
            Check if the user with user_name exists. If true return 0, if user 
            does not exists return 1.
        """
        # Check if the user exists
        users = os.listdir(self.SESSION_PATH) 

        # If the user exists return 0
        if(user_name not in users):
            return 0
        
        else:
            return 1
             
        pass

    def create_user(self,user_name):
        """
            Create a new session for user with user_name if it doesnot exist.
        """
        user_name = user_name.lower()
        if(self.user_exists(user_name)):
            print(f"CONSOLE: Cannot create the user with username {user_name} as it already exists")
            return 0
        print(f"CONSOLE: Created user with username {user_name}")
        user_path = self.SESSION_PATH/user_name
        os.mkdir(user_path)
        user_object = User(user_name,user_path)
        return user_object
         
        pass

    def delete_user(self,user_name):
        """
            Deletes the user and all his data
        """
        user_name = user_name.lower()
        if(not self.user_exists(user_name)):
            print(f"CONSOLE: Cannot delete the user with username {user_name} as does not exist")
            return 0
        
        print(f"CONSOLE: Deleting user with username {user_name}")
        shutil.rmtree(self.SESSION_PATH/user_name)

    def get_user(self,user_name):
        """
            This function will return the user object.
        """
        user_name = user_name.lower()
        user_path = self.SESSION_PATH/user_name
        if(not self.user_exists(user_name)):
            print(f"CONSOLE: Cannot retrieve the user as username {user_name} does not exist") 
            return 0

        user_object = User(user_name, user_path)
        
        return user_object
