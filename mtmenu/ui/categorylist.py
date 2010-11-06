from pymt import *
from categorybutton import CategoryButton
from config import CATEGORYLIST_SIZE, CATEGORYLIST_POSITION, CATEGORYLIST_FRICTION
from utils import get_all_categories

class CategoryList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, categories, **kwargs):
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
        kwargs.setdefault('friction', CATEGORYLIST_FRICTION)
        kwargs.setdefault('style', {'bg-color':(0,0,0,0)})
        super(CategoryList, self).__init__(**kwargs)
        
        self.add(categories)
        self.current = None
        
        
    def add(self, categories, category_to_select = None):
        self.categories = categories
        
        # Add categories on database
        for category in categories:
            self.add_widget(CategoryButton(category))
            
        # Add 'All' category selected by default
        self.add_widget(CategoryButton(None)) 
        
        # Click on selected category
        self.select_category(category_to_select)
       
    def refresh(self):
        self.clear()
        self.add(get_all_categories(), self.current)
        if not self.is_current_valid():
            from mtmenu import apps_list
            apps_list.refresh(None)
            
    def select_category(self, category_to_select = None):
        self.current = category_to_select
        
        for cat_button in self.children:
            if cat_button.category == self.current:
                cat_button.selected = True
                one_selected = True
            else:
                cat_button.selected = False
                
        # If no category was selected maybe it was deleted from database. Select 'All'
        if not one_selected:
            self.select_category(None)

    def is_current_valid(self):
        return self.current == None or any( map(lambda x: x.name==self.current.name, self.categories) )

    def order(self, categories):
        return sorted(categories, key = lambda cat: cat.name.lower(), reverse = True)
        

