from pymt import *
from settings import TOPBAR_SIZE, TOPBAR_POSITION
from ui.helpbutton import HelpButton

class TopBar(MTWidget):
    
    def __init__(self, **kwargs):
        style = {'bg-color': (0, 1, 0, 1), 'draw-background': 1}
        
        kwargs.setdefault('pos', TOPBAR_POSITION)
        kwargs.setdefault('size', TOPBAR_SIZE)
        kwargs.setdefault('style', style)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        super(TopBar, self).__init__(**kwargs)
        
        self.selected_order = 'name'
        self.name_pos = ()
        self.votes_pos = ()

        # HELP BUTTON
        self.add_widget(HelpButton(filename= 'images/help.png'))
        
    def draw(self):
        x,y = list(self.pos)
        
        # Border
        drawRoundedRectangle(pos = self.pos,
                             radius = 50,
                             size = self.size,
                             precision = 0.3, 
                             color=(1,1,1,1),
                             corners=(True,True,False,False))
        # Background
        drawRoundedRectangle(pos = (x+1, y+1),
                             radius = 50,
                             precision = 0.3,
                             size = (self.size[0]-2, self.size[1]-2), 
                             color=(0.2,0.2,0.2,1),
                             corners=(True,True,False,False))
        
        # Logo
        image = Image("images/logo.png")
        image.pos = x + 30, y + 12     
        image.draw()
        
        # Label
        drawLabel(label = 'SenseWall',
                  pos = (x+150, y+42),
                  font_size = 75,
                  center = False)
        
        # URL
        drawLabel(label = 'http://sensewall.dei.uc.pt',
                  pos = (x+165, y+15),
                  font_size = 30,
                  center = False)
        
        # Order By
        x,y = self.pos[0]+TOPBAR_SIZE[0], self.pos[1]+TOPBAR_SIZE[1]
        drawLabel(label = 'order by',
                  pos = (x-350, y-57),
                  font_size = 15,
                  center = False)
        
        if self.selected_order == 'name':
            name_image = "images/order_by_name_selected.png"
            vote_image = "images/order_by_votes.png"
        else:
            name_image = "images/order_by_name.png"
            vote_image = "images/order_by_votes_selected.png"
        
        # Order by Name button
        image = Image(name_image)
        self.name_pos = (x-470, y-110)
        image.pos = self.name_pos 
        image.draw()
        
        # Order by Votes button
        image = Image(vote_image)
        self.votes_pos = (x-318, y-110)
        image.pos = self.votes_pos   
        image.draw()
        
    def on_touch_up(self, touch):
        
        x,y = list(touch.pos)

        # Click on name button
        if x > self.name_pos[0] and x < self.name_pos[0]+150 and y > self.name_pos[1] and y < self.name_pos[1]+50:
            order = 'name'
        elif x > self.votes_pos[0] and x < self.votes_pos[0]+150 and y > self.votes_pos[1] and y < self.votes_pos[1]+50:
            order = 'value'
        else:
            return
        
        if self.selected_order == order:
            return
        
        self.selected_order = order
        self.draw()
        
        from mtmenu import apps_list
        apps_list.reorder(order)
        
        