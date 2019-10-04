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

    def check_widget(self,widget):
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

    def list_widgets(self):
        """
            List all the widgets this user has used
        """
        widgets = os.listdir(self.user_path)
        if(len(widgets) == 0):
            return None
        return widgets

    def create_widget(self,widget_name):
        widget_name = widget_name.upper()
        if(widget_name.upper() not in config.WIDGETS.keys()):
            print(f"CONSOLE: the widget {widget_name} is not defined yet")
            return 0

        if(self.check_widget(widget_name)):
            print("CONSOLE: the widget {} already exists for user {}".format(widget_name.upper(),self.user_name))
            return 0
        
        print(f"CONSOLE: The widget {widget_name} doesnot exist for user {self.user_name}")
        print("CONSOLE: Creating a new folder for user {} with for widget {}".format(self.user_name,widget_name))
        widget_path = self.user_path/widget_name
        os.mkdir(widget_path)
        widget_object = Widget(widget_name,widget_path)
        
        return widget_object
