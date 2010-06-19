from pymt import *
from appbutton import AppButton
from config import APPSLIST_NUMBER_OF_LINES, APPSLIST_SIZE, APPSLIST_POSITION, APPSLIST_FRICTION, APPSLIST_PADDING_X, APPSLIST_PADDING_Y, APPSLIST_BTN_POPUPS
from utils import get_applications


class PopupController(object):
    def __init__(self):
        self.opened = []
        
    def open(self, p):
        if len(self.opened) > APPSLIST_BTN_POPUPS:
            p = self.opened.pop()
            p.close()
        
        self.opened.insert(0,p)
        

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
        kwargs.setdefault('padding_x', APPSLIST_PADDING_X)
        kwargs.setdefault('padding_y', APPSLIST_PADDING_Y)
        kwargs.setdefault('friction', APPSLIST_FRICTION)
        kwargs.setdefault('style', {'bg-color':(0,0,0,0)})
        super(AppsList, self).__init__(**kwargs)
               
        self.apps = None
        self.current_category = None
        self.criteria = 'name'
        
        self.popup_controller = PopupController()
        
        for a in applications:
            a.is_running = False
            a.save(False, True)
        self.add(applications)
        
        
    def add(self, apps):
        ''' add widgets to the applications list '''
        self.apps = apps
        chunks = lambda lis, step:  map(lambda i: lis[i:i+step],  xrange(0, len(lis), step))

        for chunk in chunks(self.apps, APPSLIST_NUMBER_OF_LINES):
            chunk.reverse()
            for app in chunk:
                item = AppButton(app, self.popup_controller)
               
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

