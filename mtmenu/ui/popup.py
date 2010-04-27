from pymt import *
from settings import POPUP_SIZE, POPUP_POSITION

class Popup( MTPopup ):

    def __init__(self, app, **kwargs):
        self.text = "Name: %s\nCategory: %s\nOwner: %s\nLikes: %s\nDislikes: %s" % (app.name, app.category, app.owner, app.likes, app.dislikes)
        kwargs.setdefault('title', self.text)
        kwargs.setdefault('size', POPUP_SIZE)
        kwargs.setdefault('pos', POPUP_POSITION)
        kwargs.setdefault('label_sumit', 'Play')
        kwargs.setdefault('show_cancel', True)
        kwargs.setdefault('exit_on_submit', True)
        
        super(Popup, self).__init__(**kwargs)

