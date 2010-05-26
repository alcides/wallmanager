from pymt import *
from config import HELPPOPUP_POSITION, HELPPOPUP_SIZE, MAINWINDOW_SIZE

class HelpPopup(MTModalWindow):

    def __init__(self, **kwargs):
        self.app = None
        kwargs.setdefault('pos', HELPPOPUP_POSITION)
        kwargs.setdefault('size', HELPPOPUP_SIZE)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        super(HelpPopup, self).__init__(**kwargs)
        
        self.like_btn_pos = ()
        self.dislike_btn_pos = ()


    def draw (self):
        x,y = list(self.pos)
        text_size_x = self.size[0] - 40
        text_pos_x = x + 20
        
        # Cover
        drawRoundedRectangle(pos = (0,0),
                             radius = 0,
                             size = MAINWINDOW_SIZE,
                             precision = 1,
                             color = (0,0,0,0.7))
        
        # Background
        drawRoundedRectangle(pos = self.pos,
                             radius = 10,
                             size = self.size,
                             precision = 0.3, 
                             color = (1, 1, 1, 1))
        drawRoundedRectangle(pos = (self.pos[0]+2, self.pos[1]+2),
                             radius = 10,
                             size = (self.size[0]-4, self.size[1]-4),
                             precision = 0.3, 
                             color = (0, 0, 0, 1))
        
        # Text
        drawLabel(label = 'You are using SenseWall, the multi-touch wall developed by SenseBloom and the Departament of Informatics Engineering of the University of Coimbra.',
                  pos = (text_pos_x, y+self.size[1]-20),
                  font_size = 13,
                  center = False,
                  size = (text_size_x,40),
                  anchor_x = 'left',
                  anchor_y = 'top',
                  autosize = False,
                  autowidth = False,
                  autoheight = False)
        
        # SenseBloom logo
        image = Image("images/sensebloom.png")
        image.pos = x + 150, y+self.size[1]-185  
        image.draw()
        
        # SenseBloom logo
        image = Image("images/dei.png")
        image.pos = x + 410, y+self.size[1]-185  
        image.draw()
        
        # Text
        drawLabel(label = 'The goal of SenseWall is to give students a plataform for learning Human-Computer Interface (HCI) concepts and a tool for the development of interesting and creative applications.',
                  pos = (text_pos_x, y+self.size[1]-200),
                  font_size = 13,
                  center = False,
                  size = (text_size_x,40),
                  anchor_x = 'left',
                  anchor_y = 'top',
                  autosize = False,
                  autowidth = False,
                  autoheight = False)
        
        # Text
        drawLabel(label = 'For more information on how to develop applications for SenseWall and deploy them, go to http://sensewall.dei.uc.pt',
                  pos = (text_pos_x, y+self.size[1]-270),
                  font_size = 13,
                  center = False,
                  size = (text_size_x,40),
                  anchor_x = 'left',
                  anchor_y = 'top',
                  autosize = False,
                  autowidth = False,
                  autoheight = False)
        
        # Line
        drawRoundedRectangle(pos = (text_pos_x, y+self.size[1]-335),
                             radius = 0,
                             size = (text_size_x, 2),
                             precision = 1, 
                             color = (1, 1, 1, 1))
        
        # Application's tooltip text
        drawLabel(label = 'To know more about an application on the SenseWall, just do a single touch on its icon. To launch it press \'Play\' or double touch the icon.',
                  pos = (text_pos_x, y+self.size[1]-355),
                  font_size = 13,
                  center = False,
                  size = (text_size_x/2-10,40),
                  anchor_x = 'left',
                  anchor_y = 'top',
                  autosize = False,
                  autowidth = False,
                  autoheight = False)
        
        # Application's tooltip Image
        image = Image("images/app_tooltip.png")
        image.pos = text_pos_x+45, y+45 
        image.draw()
        
        #Line
        drawRoundedRectangle(pos = (x + self.size[0]/2, y+20),
                             radius = 0,
                             size = (2, 325),
                             precision = 1, 
                             color = (1, 1, 1, 1))
        # Exit gesture Text
        drawLabel(label = 'To force any application to close, use this special gesture:',
                  pos = (text_pos_x + (text_size_x/2+20), y+self.size[1]-355),
                  font_size = 13,
                  center = False,
                  size = (text_size_x/2-5,50),
                  anchor_x = 'left',
                  anchor_y = 'top',
                  autosize = False,
                  autowidth = False,
                  autoheight = False)
        
        # Exit gesture Image
        image = Image("images/exit_gesture.png")
        image.pos = text_pos_x + (text_size_x/2+40), y+25 
        image.draw()
        

    def on_touch_up(self, touch):
        x,y = list(touch.pos)
        
        if x > self.pos[0] and x < self.pos[0]+self.size[0] and y > self.pos[1] and y < self.pos[1]+self.size[1]:
            self.parent.remove_widget(self)
