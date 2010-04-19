from gesture_db import *
from application_runner import getAppRunning
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
        if self.gestures.find(gesture, 0.5) and app != None:
            print "gesture recognized"
            if app:
                print "kill app " + str(app.pid)
                subprocess.Popen("taskkill /F /T /PID %i"%app.pid , shell=True)
            


