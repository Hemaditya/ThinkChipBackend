from session import settings
from widgets import Widget
import config
import os

class User():
    """
        The class to hold the data for a user.
    """

    def __init__(self,user_name,user_path=None):
        """
            Initialize user_name and path
        """
        self.user_name = user_name
        self.user_path = user_path
        pass

    def check_user_widget(self,widget):
        """
            This module checks if a widget exists in user's session
        """
        widget = widget.upper()
        # Check if the widget is i use yet.
        if(widget not in config.WIDGETS.keys()):
            return 0
        
        # Check if the widget already exists for that user
        if(widget in os.listdir(self.user_path)):
            return 1
        return 0

    def list_user_widgets(self):
        """
            List all the widgets this user has used
        """
        widgets = os.listdir(self.user_path)
        if(len(widgets) == 0):
            return None
        return widgets

    def create_user_widget(self,widget):
        if(check_user_widget(widget)):
            print("CONSOLE: the widget {} already exists for user {}".format(widget.upper(),self.user_name))
            return 0
        
        print("CONSOLE: The widget {} doesnot exist for user {}")
        print("CONSOLE: Creating a new folder for user {} with for widget {}".format(self.user_name,widget))
        widgetpath = self.user_path/widget
        os.mkdir(widgetpath)
        return widgetpath

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
        print(f"CONSOLE: Create user with username {user_name}")
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
        os.rmdir(self.SESSION_PATH/user_name)

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