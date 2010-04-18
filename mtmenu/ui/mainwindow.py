from pymt import *

__all__ = ['MainWindow']

class MainWindow (MTWindow):
    """Menu main window"""
    
    DEFAULT_WIDTH = 2 * 1024
    DEFAULT_HEIGHT = 748
    
    def __init__(self, **kwargs):
        kwargs.setdefault('width', DEFAULT_WIDTH)
        kwargs.setdefault('height', DEFAULT_HEIGHT)
        
        super(kwargs)