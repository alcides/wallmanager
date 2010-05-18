from gesture.gesture_widget import *

class GestureScan(MTWidget):
    def __init__(self, **kwargs):
        super(GestureScan, self).__init__(**kwargs)
        self.capture = GestureWidget()
        self.add_widget(self.capture)

