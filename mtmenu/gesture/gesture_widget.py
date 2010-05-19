from pymt import *
import subprocess
from datetime import datetime

from mtmenu.application_running import is_app_running, kill_app_running
from gesture.gesture_db import *
from settings import GESTURE_ACCEPTANCE_MARGIN
from ui import projector_on, last_activity
from webmanager.appman.utils import projectors_power

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        print 'Gesture loaded'

    def on_gesture(self, gesture, touch):
        if not projector_on:
            projector_on = 1
            projectors_power(0)
        
        last_activity = datetime.now()
            
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

