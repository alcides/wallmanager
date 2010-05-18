from pymt.ui.widgets.modalwindow import MTModalWindow
from ui.votepopup import VotePopup
from threading import Timer
from utils import bring_window_to_front


class CoverWindow(MTModalWindow):

    def __init__(self, **kwargs):
        self.vote = VotePopup()
        self.TIME = 10.0
        self.timer = None
        super(CoverWindow, self).__init__(**kwargs)
        
        
    def show(self):
        from mtmenu import main_window
        main_window.add_widget( self )

    def resume(self, app):
        bring_window_to_front()
        
        self.vote.app = app
        self.add_widget( self.vote )
        self.timer = Timer(self.TIME, self.hide)
        self.timer.start()
    
        
    def hide(self):
        if self.timer:
            self.timer.cancel()        
        self.remove_widget( self.vote )
        if self.parent:
            self.parent.remove_widget( self )

