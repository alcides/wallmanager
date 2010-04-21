from gesture_list import *
from my_gesture import *
from settings import KILLER_GESTURE

class Gestures( GestureDatabase ):
    def __init__(self):
        super(Gestures, self).__init__()
        a = self.str_to_gesture(KILLER_GESTURE).strokes
        
        g = MyGesture( a[0].points )
        self.add_gesture( g.gesture )    

