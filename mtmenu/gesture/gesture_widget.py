import sys
sys.path.append("..")

from pymt import *
import subprocess
from datetime import datetime

from mtmenu.application_running import is_app_running, kill_app_running
from gesture.gesture_db import *
from config import GESTURE_ACCEPTANCE_MARGIN
from webmanager.appman.utils import projectors

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        print 'Gesture loaded'

    def on_gesture(self, gesture, touch):
        from mtmenu import projector_on, last_activity
        if not projector_on:
            projector_on = 1
            print "projectors power on"
            projectors.projectors_power(1)
        
        last_activity = datetime.now()
            
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

