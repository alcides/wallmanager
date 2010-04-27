from pymt import *
from appbutton import AppButton

class AppsList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Applications List')
        kwargs.setdefault('size', (500,500))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', True)
        kwargs.setdefault('do_y', False)
        kwargs.setdefault('h_limit', 2)
        kwargs.setdefault('w_limit',0)
        kwargs.setdefault('font_size', 12)
        self.apps = None

        super(AppsList, self).__init__(**kwargs)
        
        
    def add(self, apps):
        ''' add widgets to the applications list '''
        self.apps = apps
        
        for app in apps:
            item = AppButton(app, style = {'bg-color': (0, .2, 0, 1), 'draw-background': 1})
            self.add_widget(item)
            
    def replace(self, apps):
        ''' replace the current list of the applications with the apps provided '''
        self.clear()
        self.add(apps)

    