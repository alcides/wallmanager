from pymt.ui.widgets.modalwindow import MTModalWindow
from ui.votepopup import VotePopup
from threading import Timer
from utils import bring_window_to_front
from config import COVER_WINDOW_RESUME_TIME


class CoverWindow(MTModalWindow):

    def __init__(self, **kwargs):
        self.vote = VotePopup()
        self.timer = None
        super(CoverWindow, self).__init__(**kwargs)
        
        
    def show(self):
        from mtmenu import main_window
        main_window.add_widget( self )

    def resume(self, app, is_screensaver):
        bring_window_to_front()
        if not is_screensaver:
            self.vote.app = app
            self.add_widget( self.vote )
            self.timer = Timer(COVER_WINDOW_RESUME_TIME, self.hide)
            self.timer.start()
        else:
            self.hide()
        
    def hide(self):
        if self.timer:
            self.timer.cancel()        
        self.remove_widget( self.vote )
        if self.parent:
            self.parent.remove_widget( self )

