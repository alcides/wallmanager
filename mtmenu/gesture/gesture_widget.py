from gesture_db import *
from global_objects import getAppRunning
from pymt import *
import subprocess

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
    
    def on_gesture(self, gesture, touch):
        print 'gesture:'
        
        app = getAppRunning()
        
        # TODO: recognize gesture and replace or with and
        if self.gestures.find(gesture, 0.5) or app != None:
            print "gesture recognized"
            print "kill app "+str(app.pid)
            subprocess.Popen("taskkill /F /T /PID %i"%app.pid , shell=True)
            


