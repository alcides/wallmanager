from pymt import *

class CategoryList (MTKineticList):
    
    """Widget to handle applications list"""

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Categories')
        kwargs.setdefault('size', (150,460))
        kwargs.setdefault('pos', (20,20))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('do_x', False)
        kwargs.setdefault('do_y', True)
        kwargs.setdefault('h_limit', 0)
        kwargs.setdefault('w_limit', 1)
        kwargs.setdefault('font_size', 14)

        super(CategoryList, self).__init__(**kwargs)
