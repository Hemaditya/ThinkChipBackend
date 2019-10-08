"""    This is less complicated version of creating Sessions and users
"""
import pathlib
import os
import config
import shutil

def check_user(user):
    ''' This function checks if the user exists or not '''

    """
        Inputs:
            f: str or Path object
            - if f is a string, it is assumed to be username.
            - if f is a Path object, it is assumed to be the path to the user's directory

        Outputs:
            - returns 0 if the user does not exist.
            - returns path if the user exists.
    """
    path = user
    if(type(user) == str):
        user = user.lower()
        path = config.SESSION_PATH/user
    if not os.path.isdir(path):
        print(f"CONSOLE: The user {user} does not exist.")
        return 0
    print(f"CONSOLE: The user {user} exists.")
    return path

def create_user(username):
    ''' This function creates a new folder for the user if he does not exist '''

    """
        Inputs:
            username: string
            - The username of the person for whom you wanna create the folder.

        Outputs:
            This function returns 0 if the folder is not created else returns the newly created user path. 
    """
    
    user_path = check_user(username)
    if user_path != 0:
        print(f"CONSOLE: Cannot create the folder for {username} as it already exists")
        return 0
    user_path = config.SESSION_PATH/username 
    os.mkdir(user_path)
    print(f"CONSOLE: The folder for {username} created successfully.")
    return user_path

def delete_user(username):
    ''' This function deletes all the data of the user '''

    """
        Inputs:
            username: string or Path
            - The username of the person whose data you want to delete.

        Outputs:
            This function returns 0 if the data is deleted, else 1.
    """

    user_path = check_user(username)
    if user_path == 0:
        print(f"CONSOLE: Cannot delete the data for {username} as it does not exists")
        return 0

    shutil.rmtree(user_path)
    print(f"CONSOLE: The folder for {username} deleted successfully.")
    return 1

def check_widget(user, widget):
    ''' This function checks if a widget exists or not for a user.'''

    """
        Inputs:
            f: str or Path object
            - if f is a string, it is assumed to be username.
            - if f is a Path object, it is assumed to be the path to the user's directory

        Outputs:
            - returns -1 if the user does not exist.
            - returns 0 if the widget does not exists for the user.
            - returns 1 if the widget exists for the user.
    """
    user_path = check_user(user)

    if(user_path == 0):
        return 0

    widget_path = user_path/widget
    if(widget == str):
        widget = widget.lower()
        widget_path = user_path/widget
    if not os.path.isdir(widget_path):
        print(f"CONSOLE: The widget {widget} does not exist.")
        return 0

    print(f"CONSOLE: The widget {widget} exists.")
    return widget_path


def delete_widget(user,widget):
    ''' This function deletes a widget from the user '''

    """
        user: str or Path object
        - if user is a string, it is assumed to be username.
        - if user is a Path object, it is assumed to be the path to the user's directory

        widget: str or Path object
        - if widget is a string, it is assumed to be widgets name.
        - if widget is a Path object, it is assumed to be the path to the widgets's directory
    """
    widget_path = check_widget(user,widget)
    if widget_path == 0:
        print(f"CONSOLE: Cannot delete the widget {widget}") 
        return 0

    shutil.rmtree(widget_path)
    print(f"CONSOLE: Widget {widget} successfully deleted.") 


def add_widget(user, widget):
    ''' This function adds a new widget to the user '''

    """
        user: str or Path object
        - if user is a string, it is assumed to be username.
        - if user is a Path object, it is assumed to be the path to the user's directory

    """

    widget_path = check_widget(user,widget)
    if widget_path != 0:
        print(f"CONSOLE: Cannot create the widget {widget} as the widget already exists") 
        return 0

    os.mkdir(widget_path)
    print(f"CONSOLE: Widget {widget} successfully created.") 

    return widget_path
