from pymt.ui.widgets.scatter import MTScatterWidget
from mtmenu.settings import SCATTER_POSITION, SCATTER_SIZE
from mtmenu.ui.votepopup import VotePopup
from threading import Timer


class Scatter( MTScatterWidget ):
    
    def __init__(self, **kwargs):
        #kwargs.setdefault('filename', '../images/wallpaper.png')
        kwargs.setdefault('pos', SCATTER_POSITION)
        kwargs.setdefault('size', SCATTER_SIZE)
        kwargs.setdefault('do_rotation', False)
        #kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        self.vote = VotePopup()
        self.timer = Timer(10.0, self.display)
        super(Scatter, self).__init__(**kwargs)
        
        
    def resume(self, app):
        self.vote.app = app
        self.get_root_window().add_widget( self.vote )
        self.timer.start()
    
        
    def display(self):
        self.timer.cancel()
        self.get_root_window().remove_widget( self.vote )
        self.show()

 
    def __call__(self):
        return self

