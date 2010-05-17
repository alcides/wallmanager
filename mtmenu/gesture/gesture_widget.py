from mtmenu.application_running import is_app_running, kill_app_running
from gesture.gesture_db import *
from pymt import *
import subprocess
from settings import GESTURE_ACCEPTANCE_MARGIN

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        print 'Gesture loaded'
    
    def on_gesture(self, gesture, touch):
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

