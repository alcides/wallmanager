from gesture_list import *
from my_gesture import *
from settings import GESTURE_KILLER

class Gestures( GestureDatabase ):
    def __init__(self):
        super(Gestures, self).__init__()
        a = self.str_to_gesture(GESTURE_KILLER).strokes
        
        g = MyGesture( a[0].points )
        self.add_gesture( g.gesture )    

