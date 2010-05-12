from pymt import *
from mtmenu.settings import WALL_DEFAULT_WIDTH, WALL_DEFAULT_HEIGHT

__all__ = ['MainWindow']

class MainWindow (MTWindow):
    """Menu main window"""
    def __init__(self, **kwargs):
        kwargs.setdefault('width', WALL_DEFAULT_WIDTH)
        kwargs.setdefault('height', WALL_DEFAULT_HEIGHT)
        super(kwargs)
