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
        self.categories = None
        self.current = None
        super(CategoryList, self).__init__(**kwargs)
        
        
    def add(self, categories):
        self.categories = categories
        style = {'bg-color': (0, 1, 0, 1), 'draw-background': 1, 'draw-border': True, 'border-radius': 5}
        for category in categories:
            self.add_widget( CategoryButton(category, style = style) )        
        self.add_widget( CategoryButton(None, style=style) )
        
       
    def refresh(self): 
        self.clear()
        self.add( get_all_categories() )
        if not self.is_current_valid():
            from mtmenu.ui import apps_grid
            apps_grid.refresh(None)


    def is_current_valid(self):
        return self.current == None or any( map(lambda x: x.name==self.current.name, self.categories) )
        

    def order(self, categories):
        return sorted(categories, key = lambda cat: cat.name.lower(), reverse= True)
        

