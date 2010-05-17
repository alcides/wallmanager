from pymt import *
from appbutton import AppButton
from settings import APPSLIST_NUMBER_OF_LINES, APPSLIST_SIZE, APPSLIST_POSITION
from utils import get_applications

class AppsList(MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, applications, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('size', APPSLIST_SIZE)
        kwargs.setdefault('pos', APPSLIST_POSITION)
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', True)
        kwargs.setdefault('do_y', False)
        kwargs.setdefault('h_limit', APPSLIST_NUMBER_OF_LINES)
        kwargs.setdefault('w_limit',0)
        kwargs.setdefault('font_size', 12)
        kwargs.setdefault('padding_x', 300)
        kwargs.setdefault('padding_y', 50)
        kwargs.setdefault('style', {'bg-color':(0,0,0,0)})
        super(AppsList, self).__init__(**kwargs)
               
        self.apps = None
        self.current_category = None
        self.criteria = 'name'
        
        self.add(applications)
        
        
    def add(self, apps):
        ''' add widgets to the applications list '''
        self.apps = apps
        chunks = lambda lis, step:  map(lambda i: lis[i:i+step],  xrange(0, len(lis), step))

        for chunk in chunks(self.apps, APPSLIST_NUMBER_OF_LINES):
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
            
            

    def reorder(self, sort_criteria = None):
        if sort_criteria:
            self.criteria = sort_criteria
        self.clear()
        self.apps = get_applications( self.current_category, self.criteria == 'value')
        self.add( self.apps )

    def __call__(self):
        return self

