from pymt import *
from categorybutton import CategoryButton
from settings import CATEGORYLIST_SIZE, CATEGORYLIST_POSITION
from utils import get_all_categories

class CategoryList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, apps_list, categories, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', False)
        kwargs.setdefault('do_y', True)
        kwargs.setdefault('h_limit', 0)
        kwargs.setdefault('w_limit', 1)
        kwargs.setdefault('font_size', 14)
        kwargs.setdefault('size', CATEGORYLIST_SIZE)
        kwargs.setdefault('pos', CATEGORYLIST_POSITION)
        kwargs.setdefault('style', {'bg-color':(0,0,0,0)})
        super(CategoryList, self).__init__(**kwargs)
        
        self.apps_list = apps_list
        self.add(categories)
        self.current = None
        
        
    def add(self, categories):
        self.categories = categories
        for category in categories:
            self.add_widget( CategoryButton(category) )        
        self.add_widget( CategoryButton(None) )
        
       
    def refresh(self): 
        self.clear()
        self.add( get_all_categories() )
        if not self.is_current_valid():
            from mtmenu import apps_list
            apps_list.refresh(None)


    def is_current_valid(self):
        return self.current == None or any( map(lambda x: x.name==self.current.name, self.categories) )
        

    def order(self, categories):
        return sorted(categories, key = lambda cat: cat.name.lower(), reverse= True)
        

