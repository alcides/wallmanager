from pymt import *
from settings import MAINWINDOW_SIZE

class BackgroundImage(MTScatterImage):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size', MAINWINDOW_SIZE)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('auto_bring_to_front', False)
        super(BackgroundImage, self).__init__(**kwargs)

