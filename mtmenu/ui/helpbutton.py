from pymt.ui.widgets.composed.modalpopup import MTModalPopup
from pymt.ui.widgets.button import MTImageButton
from settings import TOPBAR_POSITION, TOPBAR_SIZE


class HelpButton(MTImageButton):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', 'images/help.png')
        kwargs.setdefault('size', (68,68))
        kwargs.setdefault('pos', (TOPBAR_SIZE[0]-90, TOPBAR_POSITION[1]+43))
        
        self.pop = MTModalPopup(title='Need help?', content='I wont help you')
        super(HelpButton, self).__init__(**kwargs)
        
        
    def on_press(self, touch):
        self.get_root_window().add_widget( self.pop )    

