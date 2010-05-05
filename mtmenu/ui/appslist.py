from pymt import *
from appbutton import AppButton
from utils import get_applications
from mtmenu.settings import LINES_IN_APPS_GRID


class AppsList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('size', (500,500))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', True)
        kwargs.setdefault('do_y', False)
        kwargs.setdefault('h_limit', LINES_IN_APPS_GRID)
        kwargs.setdefault('w_limit',0)
        kwargs.setdefault('font_size', 12)
        kwargs.setdefault('padding_x', 20)
        kwargs.setdefault('padding_y', 45)        
        self.apps = None
        self.current_category = None
        self.criteria = 'name'
        super(AppsList, self).__init__(**kwargs)
        
        
    def add(self, apps):
        ''' add widgets to the applications list '''
        self.apps = apps
        chunks = lambda lis, step:  map(lambda i: lis[i:i+step],  xrange(0, len(lis), step))

        for chunk in chunks(self.apps, LINES_IN_APPS_GRID):
            chunk.reverse()
            for app in chunk:
                item = AppButton(app)
                self.add_widget(item)

                   
    def refresh(self, category):
        ''' replace the current list of the applications with the apps provided '''  
        if category == self.current_category:
            return            
        self.current_category = category
        self.reorder()
            
            
    def reorder(self, sort_criteria=None):
        if sort_criteria:
            self.criteria = sort_criteria
        self.clear()
        self.apps = get_applications( self.current_category, self.criteria == 'value')
        self.add( self.apps )
        
          
            
    def __call__(self):
        return self

