import sys
sys.path.append("..")

from pymt import *
import subprocess
from datetime import datetime

from mtmenu.application_running import is_app_running, kill_app_running

from gesture.gesture_db import *
from config import GESTURE_ACCEPTANCE_MARGIN, PRODUCTION, UNAVAILABLE_PROJECTORS_TIME
from webmanager.appman.utils import projectors


class GestureWidget( MTGestureWidget ):
    def __init__(self, checker):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        self.activity_checker = checker
        print 'Gesture loaded'

    def on_gesture(self, gesture, touch):

        print "PROJECTORS STATE: ", self.activity_checker.projectors_on
        if not self.activity_checker.projectors_on:
            print 'Turning Projectors On'
            self.activity_checker.turn_projectors_power(1)
        self.activity_checker.set_last_activity()
            
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

