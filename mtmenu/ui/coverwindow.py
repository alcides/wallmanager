from pymt.ui.widgets.modalwindow import MTModalWindow
from mtmenu.ui.votepopup import VotePopup
from threading import Timer
from mtmenu.utils import bring_window_to_front



class CoverWindow( MTModalWindow ):

    def __init__(self, **kwargs):
        self.vote = VotePopup()
        self.TIME = 10.0
        super(CoverWindow, self).__init__(**kwargs)
        
        
    def show(self):
        from mtmenu.ui import main_window
        main_window.add_widget( self )
        
        
#    def on_touch_up(self, touch):
#        Timer(0.5, self.hide).start()

        
    
    def resume(self, app):
        bring_window_to_front()  
        self.vote.app = app
        self.add_widget( self.vote )
        self.timer = Timer(self.TIME, self.hide)
        self.timer.start()
    
        
    def hide(self):
        self.timer.cancel()        
        self.remove_widget( self.vote )
        if self.parent:
            self.parent.remove_widget( self )

