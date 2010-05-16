from pymt import *
from settings import CATEGORYLIST_SIZE

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
        from ui import apps_list
        apps_list.refresh(self.category)
        

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
        drawLabel(label = self.label,
                  pos = (x+20, y + 8),
                  font_size = 15,
                  center = False)
