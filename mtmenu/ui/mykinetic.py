from pymt import *


class MyButton(MTButton):

    def __init__(self, **kwargs):
        kwargs.setdefault('label', 'lalaaaaa')
        kwargs.setdefault('pos', (10,10))
        kwargs.setdefault('size', (100,100))
        super(MyButton, self).__init__(**kwargs)

    
    def draw_background(self):
        drawCSSRectangle(pos=self.pos, size=self.size, style=self.style)


    def draw_label(self, dx=0, dy=0):
        pos = list(self.center)

        print pos
        w, h = drawLabel(label='laaaaaa', pos=pos)

        
        
    def draw(self):
        self.draw_background()
        self.draw_label()
        self.image = Image( "/home/diogo/Desktop/DEI/gps/wallmanager/mtmenu/images/icon.jpg")
        self.image.pos = list(self.center)
        #self.size = self.image.size
        self.image.draw()


class MyKinetic( MyButton, MTKineticObject ):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
