from pymt.ui.widgets.button import MTImageButton
from pymt.ui.widgets.composed.modalpopup import MTModalPopup


class ImageButton( MTImageButton ):

    def __init__(self, **kwargs):
        kwargs.setdefault('filename', 'images/help.png')
        kwargs.setdefault('scale', 1)
        self.pop = MTModalPopup(title='You want help?', content='I wont help you')
        super(ImageButton, self).__init__(**kwargs)
        
        
    def on_press(self, touch):
        self.parent.add_widget(self.pop)

