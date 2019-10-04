from session import settings
from widgets import Widget
import config
import os

class User():
    """
        The class to hold the data for a user.
    """

    def __init__(self,username,user_path=None):
        """
            Initialize username and path
        """
        self.username = username
        self.user_path = user_path
        pass

    def add_user_widget(self,widget):
        """
            This module adds widget folder to the user's session.
        """
        widget = widget.upper()

        # Check if the widget is i use yet.
        if(widget not in config.WIDGETS.keys()):
            return 0
        
        # Check if the widget already exists for that user
        if(widget in os.listdir(self.user_path)):
            return 1

        # If that widget does not exist for that user, then create a new folder for that widget.
        widget_path = self.user_path/widget
        os.mkdir(widget_path)
        widget = Widget(widget_path)

        return widget


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

    def create_user(self,username):
        """
            Create a new session for user with username if it doesnot exist.
        """
        username = username.lower()
        user_path = self.SESSION_PATH/username
        os.mkdir(user_path)
        user_object = User(username,user_path)
        return user_object
         
        pass

