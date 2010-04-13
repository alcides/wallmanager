from pymt import *
from gesture_db import *


class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
    
    def on_gesture(self, gesture, touch):
        print 'gesture'
        #print self.gestures.gesture_to_str( gesture )
        if self.gestures.find(gesture, 0.5):
            print "gesture recognized"

