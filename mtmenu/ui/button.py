from pymt import *


class Button( MTButton ):

    def __init__( self, **args ):
        args.setdefault('label', 'button')
        args.setdefault('width', 90)
        args.setdefault('height', 40)
        args.setdefault('font_size', 16)
        super(Button, self).__init__(**args)



    def on_press( self, touch ):
        print self.label + ':: press'


    def on_release( self, touch ):
        print self.label + ':: release'