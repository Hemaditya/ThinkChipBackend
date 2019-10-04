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
