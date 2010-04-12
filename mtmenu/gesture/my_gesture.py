from pymt import *

class MyGesture():
    def __init__(self, *strokes):
        self.gesture = Gesture()
        self.gesture.add_stroke([y for x in strokes for y in x ])
        self.gesture.normalize()
        
    def get_points(self):
        for i in self.gesture.strokes:
            print i.points    

