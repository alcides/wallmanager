from pymt import *

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

        super(AppsList, self).__init__(**kwargs)
