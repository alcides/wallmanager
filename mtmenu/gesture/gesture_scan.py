from gesture.gesture_widget import *

class GestureScan(MTWidget):
    def __init__(self, checker, **kwargs):
        super(GestureScan, self).__init__(**kwargs)
        self.capture = GestureWidget(checker)
        self.add_widget(self.capture)

