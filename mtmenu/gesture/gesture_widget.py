from gesture_db import *
from application_running import getAppRunning, killAppRunning
from pymt import *
import subprocess

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
    
    def on_gesture(self, gesture, touch):
        print 'gesture:'
        
        # TODO: recognize gesture and replace or with and
        if self.gestures.find(gesture, 0.5) and getAppRunning():
            print "gesture recognized"
            killAppRunning()
            


