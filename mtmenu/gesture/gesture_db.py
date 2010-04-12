from gesture_list import *
from my_gesture import *

class Gestures( GestureDatabase ):
    def __init__(self):
        super(Gestures, self).__init__()
        #a = self.str_to_gesture(STR).strokes
        g = MyGesture( join(RIGHT, DOWN), join(LEFT, DOWN) )
        self.add_gesture( g.gesture )    

