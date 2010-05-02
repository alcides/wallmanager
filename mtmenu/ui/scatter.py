from pymt.ui.widgets.scatter import MTScatterWidget
from mtmenu.settings import SCATTER_POSITION, SCATTER_SIZE
from mtmenu.ui.coverwindow import CoverWindow


class Scatter( MTScatterWidget):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('pos', SCATTER_POSITION)
        kwargs.setdefault('size', SCATTER_SIZE)
        kwargs.setdefault('do_rotation', False)
        #kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        
        super(Scatter, self).__init__(**kwargs)
        
        
    def __call__(self):
        return self

