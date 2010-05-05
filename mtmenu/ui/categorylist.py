from pymt import *
from categorybutton import CategoryButton
from utils import *

class CategoryList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', False)
        kwargs.setdefault('do_y', True)
        kwargs.setdefault('h_limit', 0)
        kwargs.setdefault('w_limit', 1)
        kwargs.setdefault('font_size', 14)
        super(CategoryList, self).__init__(**kwargs)
        
        
    def add(self, categories):
        style = {'bg-color': (0, 1, 0, 1), 'draw-background': 1, 'draw-border': True, 'border-radius': 5}
        for category in self.order( categories ):
            self.add_widget( CategoryButton(category, style = style) )        
        self.add_widget( CategoryButton(None, style=style) )
        
       
    def refresh(self):
        print 'la'
        self.clear()
        print 'ca'
        self.add( getAllCategories() )
        print 'ka'


    def order(self, categories):
        return sorted(categories, key = lambda cat: cat.name.lower(), reverse= True)
        

