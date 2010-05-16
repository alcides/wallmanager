from ui.popup import Popup
from settings import VOTEPOPUP_POSITION, VOTEPOPUP_SIZE

class VotePopup( Popup ):

    def __init__(self, **kwargs):
        self.app = None
        kwargs.setdefault('title', 'What do you think about this application?')
        kwargs.setdefault('size', VOTEPOPUP_SIZE)
        kwargs.setdefault('pos', VOTEPOPUP_POSITION)
        kwargs.setdefault('label_submit', 'Like')
        kwargs.setdefault('label_cancel', 'Dislike')
        kwargs.setdefault('anchor_x', 'center')
        kwargs.setdefault('show_cancel', True)
        kwargs.setdefault('exit_on_submit', True)
        super(VotePopup, self).__init__(**kwargs)

    def on_submit(self):
        self.app.vote(True)
        self.resume()
        
        
    def on_cancel(self):
        self.app.vote(False)
        self.resume()


    def resume(self):
        self.parent.hide()

