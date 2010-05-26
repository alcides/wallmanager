from pymt import *
from config import CATEGORYLIST_SIZE, CATEGORYLIST_LABEL_SIDES_MARGIN, CATEGORYLIST_LABEL_FONT_SIZE

class CategoryButton(MTKineticItem):

    def __init__(self, cat, **kwargs):
        self.category = cat
        
        if cat:
            kwargs.setdefault('label', cat.name)
        else:
            kwargs.setdefault('label', 'All')
        kwargs.setdefault('size', (CATEGORYLIST_SIZE[0],40))
        kwargs.setdefault('deletable', False)
        
        super(CategoryButton, self).__init__(**kwargs)

    def on_press( self, touch ):
        from mtmenu import apps_list
        apps_list.refresh(self.category)
        self.parent.current = self.category
        

    def on_release( self, touch ):
        return
    
    def draw (self):
        x,y = list(self.pos)
        
        # Background
        drawRoundedRectangle(pos = self.pos,
                             radius = 5,
                             precision = 0.3,
                             size = (self.size[0]-10, self.size[1]), 
                             color=(0.447,0.447,0.447,1),
                             corners=(False,True,True,False))
        
        # Bottom Line
        points = [x, y+100] + [x+self.size[0], y+100]
        colors = [(0.6,0.6,0.6,1),(0.439,0.439,0.439,1)]
        drawLine(points, 10, colors)
        
        # Label
        label_margin = CATEGORYLIST_LABEL_SIDES_MARGIN
        label_changed = False
        label_obj = MTLabel(label = self.label,
                            pos = (x+label_margin, y+8),
                            font_size = CATEGORYLIST_LABEL_FONT_SIZE,
                            autowidth = True)
        label_max_width = self.size[0] - label_margin*2
        
        while label_obj.width > label_max_width:

            self.label = self.label[:-1]
            
            label_changed = True
            label_obj = MTLabel(label = "%s..." % self.label,
                                pos = (x+label_margin, y+8),
                                font_size = CATEGORYLIST_LABEL_FONT_SIZE,
                                autowidth = True)
        
        if label_changed:
            self.label = "%s..." % self.label
        label_obj.draw()
