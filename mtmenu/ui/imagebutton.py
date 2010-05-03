from pymt.ui.widgets.composed.modalpopup import MTModalPopup
from pymt.ui.widgets.button import MTImageButton


class ImageButton( MTImageButton ):
    
    def __init__(self, **kwargs):
        self.pop = MTModalPopup(title='Need help?', content='I wont help you')
        super(ImageButton, self).__init__(**kwargs)
        
        
    def on_press(self, touch):
        self.get_root_window().add_widget( self.pop )    

