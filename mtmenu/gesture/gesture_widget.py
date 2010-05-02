from application_running import getAppRunning, killAppRunning
from gesture.gesture_db import *
from pymt import *
import subprocess
from mtmenu.settings import ACCEPTANCE_MARGIN

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
    
    def on_gesture(self, gesture, touch):
        #print 'gesture:\n'
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, ACCEPTANCE_MARGIN) and getAppRunning():
            print "gesture recognized"
            killAppRunning()
            


