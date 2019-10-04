from session import settings
from widgets import Widget
import config
import os
import shutil # to use rmtree

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
        """
            Create a new folder for the user for that widget widget_name
        """
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

    def delete_widget(self,widget_name):
        """
            This function will delete a widget from the user.
        """

        widget_name = widget_name.upper()
        if(widget_name not in os.listdir(self.user_path)):
            print(f"CONSOLE: Cannot delete as the widget {widget_name} does not exist for user {self.user_name}")
            return 0

        shutil.rmtree(self.user_path/widget_name)
        print(f"CONSOLE: Successfully deleted the data for the widget {widget_name} for user {self.user_name}")

        return 1

    def get_widget(self,widget_name):
    """
        Retrieve the widget and return its object if it exists for the user
    """

        widget_name = widget_name.upper()
        if(widget_name not in os.listdir(self.user_path)):
            print(f"CONSOLE: Cannot get the widget {widget_name} as it does not exist for user {self.user_name}")
            return 0

        widget_path = self.user_path/widget_path
        widget_object = Widget(widget_name,widget_path)

        return widget_object
