from pymt import *


class CategoryButton( MTKineticItem ):

    def __init__( self, **kwargs ):
        kwargs.setdefault('label', 'button')
        kwargs.setdefault('size', (120,40))
        kwargs.setdefault('font_size', 12)
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('anchor_x', 'center')
        kwargs.setdefault('anchor_y', 'middle')
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        super(CategoryButton, self).__init__(**kwargs)



    def on_press( self, touch ):
        print self.label + ':: press'


    def on_release( self, touch ):
        print self.label + ':: release'
