"""
    This Widget is a global class and all other widgets will subclass this one
"""

class Widget():
    """
        This Widget class, which will hold the data and specifications required 
        to initialize and use Widgets and create your own widgets too.
    """

    def __init__(self,widget,path=None):
        """
            Initialize the name of the widget.
        """
        self.widget_name = widget
        self.widget_path = path
        pass

