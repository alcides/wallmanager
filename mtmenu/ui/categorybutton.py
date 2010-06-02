from pymt import *
from config import CATEGORYLIST_SIZE, CATEGORYLIST_LABEL_SIDES_MARGIN, CATEGORYLIST_LABEL_FONT_SIZE
from utils import get_trimmed_label_widget

class CategoryButton(MTKineticItem):

    def __init__(self, cat, **kwargs):
        self.category = cat
        
        if cat:
            kwargs.setdefault('label', cat.name)
        else:
            kwargs.setdefault('label', 'All')
        kwargs.setdefault('size', (CATEGORYLIST_SIZE[0],40))
        kwargs.setdefault('deletable', False)
        
        self.selected = False
        
        super(CategoryButton, self).__init__(**kwargs)

    def on_press(self, touch):
        from mtmenu import apps_list
        apps_list.refresh(self.category)
        self.parent.select_category(self.category)
        

    def on_release( self, touch ):
        return
    
    def draw (self):
        x,y = list(self.pos)
        
        # Background
        if self.selected:
            bg_color = (0.965, 0.573, 0.118, 1) # Laranja do logotipo
        else:
            bg_color = (0.447,0.447,0.447,1) # Cinzento
        
        drawRoundedRectangle(pos = self.pos,
                             radius = 5,
                             precision = 0.3,
                             size = (self.size[0]-10, self.size[1]), 
                             color = bg_color,
                             corners=(False,True,True,False))
        
        # Bottom Line
        points = [x, y+100] + [x+self.size[0], y+100]
        colors = [(0.6,0.6,0.6,1),(0.439,0.439,0.439,1)]
        drawLine(points, 10, colors)
        
        # Label
        label_margin = CATEGORYLIST_LABEL_SIDES_MARGIN
        label_max_width = self.size[0] - label_margin*2
        label_obj, self.label = get_trimmed_label_widget(text = self.label,
                                                         position = (x+label_margin, y+8),
                                                         font_size = CATEGORYLIST_LABEL_FONT_SIZE,
                                                         max_width = label_max_width)
        label_obj.draw()