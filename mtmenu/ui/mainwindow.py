from pymt import *
from config import MAINWINDOW_SIZE, MAINWINDOW_POSITION
from ui.topbar import TopBar
from gesture.gesture_scan import GestureScan


class MainWindow(MTWindow):
    """Menu main window"""
    def __init__(self, **kwargs):
        kwargs.setdefault('size', MAINWINDOW_SIZE)
        kwargs.setdefault('pos', MAINWINDOW_POSITION)
        
        super(MainWindow, self).__init__(**kwargs)
