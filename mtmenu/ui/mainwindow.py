from pymt import *

__all__ = ['MainWindow']

class MainWindow (MTWindow):
    """Menu main window
    
    Default width: 1024 * 2
    Default height: 748 * 2
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('width', 1024 * 2)
        kwargs.setdefault('height', 748 * 2)
        
        super(kwargs)