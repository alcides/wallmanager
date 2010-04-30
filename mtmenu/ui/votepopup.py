from pymt import *
from threading import Timer


class VotePopup( MTPopup ):

    def __init__(self, **kwargs):
        self.app = None
        kwargs.setdefault('title', 'Vote Wall')
        kwargs.setdefault('size', (215,100))
        kwargs.setdefault('pos', (200,200))
        kwargs.setdefault('label_submit', 'Like')
        kwargs.setdefault('label_cancel', 'Dislike')
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
        from mtmenu.ui import scatter
        scatter.display()

