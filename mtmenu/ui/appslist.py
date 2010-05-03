from pymt import *
from appbutton import AppButton


class AppsList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('size', (500,500))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', True)
        kwargs.setdefault('do_y', False)
        kwargs.setdefault('h_limit', 2)
        kwargs.setdefault('w_limit',0)
        kwargs.setdefault('font_size', 12)
        self.apps = None
        self.current_category = None
        self.criteria = 'name'
        super(AppsList, self).__init__(**kwargs)
        
        
    def add(self, apps):
        ''' add widgets to the applications list '''
        self.apps = self.order(apps)
        chunks = lambda lis, step:  map(lambda i: lis[i:i+step],  xrange(0, len(lis), step))

        for chunk in chunks(self.apps, 2):
            chunk.reverse()
            for app in chunk:
                item = AppButton(app, style = {'bg-color': (0, 0, 0, 1), 'draw-background': 0, 'draw-border': True, 'border-radius': 10})
                self.add_widget(item)

                   
    def refresh(self, category):
        ''' replace the current list of the applications with the apps provided '''  
        if category == self.current_category:
            return          
        self.clear()  
        self.current_category = category
        
        from utils import getApplications
        self.add( getApplications(self.current_category) )
            
            
    def reorder(self, order):
        if order != self.criteria:
            self.clear() 
            self.criteria = order
            self.add( self.apps )
          
                    
    def order(self, apps):
        return sorted(apps, key = lambda app: eval('app.'+self.criteria), reverse= True)
                
            
    def __call__(self):
        return self

