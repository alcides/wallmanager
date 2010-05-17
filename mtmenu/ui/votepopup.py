from pymt import *
from settings import VOTEPOPUP_POSITION, VOTEPOPUP_SIZE, VOTEPOPUP_QUESTION
from settings import VOTEPOPUP_BTN_LIKE_COLOR, VOTEPOPUP_BTN_DISLIKE_COLOR, VOTEPOPUP_BTN_SIZE

class VotePopup(MTWidget):

    def __init__(self, **kwargs):
        self.app = None
        kwargs.setdefault('pos', VOTEPOPUP_POSITION)
        kwargs.setdefault('size', VOTEPOPUP_SIZE)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        super(VotePopup, self).__init__(**kwargs)
        
        self.like_btn_pos = ()
        self.dislike_btn_pos = ()


    def resume(self):
        self.parent.hide()


    def draw (self):
        x,y = list(self.pos)
        
        # Background
        drawRoundedRectangle(pos = self.pos,
                             radius = 10,
                             size = self.size,
                             precision = 0.3, 
                             color = (1, 1, 1, 1),
                             corners=(True,True,True,True))
        drawRoundedRectangle(pos = (self.pos[0]+2, self.pos[1]+2),
                             radius = 10,
                             size = (self.size[0]-4, self.size[1]-4),
                             precision = 0.3, 
                             color = (0, 0, 0, 1),
                             corners=(True,True,True,True))
        
        # Question label
        drawLabel(label = VOTEPOPUP_QUESTION,
                  pos = (x + (self.size[0] / 2), y + self.size[1] - 35),
                  font_size = 20,
                  center = True)
        
        # Like\Dislike button
        btn_size = VOTEPOPUP_BTN_SIZE
        btn_pos_y = y + 30
        btn_pos_x1 = x + ((self.size[0] - (btn_size[0]*2 + 10)) / 2)
        btn_pos_x2 = btn_pos_x1 + btn_size[0] + 10
        
        self.like_btn_pos = (btn_pos_x1, btn_pos_y)
        self.dislike_btn_pos = (btn_pos_x2, btn_pos_y)
        
        # Like
        drawRoundedRectangle(pos = self.like_btn_pos,
                             radius = 10,
                             size = btn_size,
                             precision = 0.3, 
                             color = VOTEPOPUP_BTN_LIKE_COLOR,
                             corners=(True,True,True,True))
        drawLabel(label = 'Like',
                  pos = (btn_pos_x1 + (btn_size[0]/2), btn_pos_y + (btn_size[1] / 2)),
                  font_size = 35,
                  center = True)
        
        #Dislike
        drawRoundedRectangle(pos = self.dislike_btn_pos,
                             radius = 10,
                             size = btn_size,
                             precision = 0.3, 
                             color = VOTEPOPUP_BTN_DISLIKE_COLOR,
                             corners=(True,True,True,True))
        drawLabel(label = 'Dislike',
                  pos = (btn_pos_x2 + (btn_size[0]/2), btn_pos_y + (btn_size[1] / 2)),
                  font_size = 35,
                  center = True)
        

    def on_touch_up(self, touch):
        
        x,y = list(touch.pos)
        a,b = list(VOTEPOPUP_BTN_SIZE)
        
        # click on like button
        if x > self.like_btn_pos[0] and x < self.like_btn_pos[0]+a and y > self.like_btn_pos[1] and y < self.like_btn_pos[1]+b:
            self.app.vote(True)
            self.resume()
        # click on dislike button
        elif x > self.dislike_btn_pos[0] and x < self.dislike_btn_pos[0]+a and y > self.dislike_btn_pos[1] and y < self.dislike_btn_pos[1]+b:
            self.app.vote(False)
            self.resume()
