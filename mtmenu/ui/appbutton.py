from pymt import *
from mtmenu.ui.apppopup import AppPopup
from threading import Timer


class AppButton(MTKineticItem):
    """Widget representing an application on main window. 
    
    Arguments:
        app -- Application object attached to this widget
        kwargs -- Button properties, most of them inherited from MTButton
    
    This widget should be added to AppsGrid on Menu's UI construction"""
    def __init__(self, app, **kwargs):
        kwargs.setdefault('label', unicode(app))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('anchor_x', 'center')
        kwargs.setdefault('anchor_y', 'middle')
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('size', (100,100))        
        
        self.double_tap_detected = False
        self.app = app
        self.pop = None
      
        
        super(AppButton, self).__init__(**kwargs)
        


    """Execute application on double click
       Open popup on single click"""
    def on_press( self, touch ):  
        self.double_tap_detected = touch.is_double_tap
        if touch.is_double_tap:
            self.pop = None
            self.open_app()
                        
        #if single tap and popup not already open
        elif not self.pop:  
            self.pop = AppPopup(self.app, pos = self.pos)
            Timer(0.5, self.open_popup).start() #make sure is not a double tap



    def open_popup(self):
        if self.double_tap_detected:
            return  
            
        self.get_root_window().add_widget(self.pop)
        self.pop = None



    def open_app(self):
        print '\nLoading %s...\n' % unicode(self.app)
        print 'ID: %i' % self.app.id
        print 'Path: %s\n' % self.app.get_extraction_fullpath()
        print 'Boot file: %s\n' % self.app.get_boot_file()
        self.app.execute()
        
        #refresh cstegory in main thread
        from mtmenu.ui import categories_list
        categories_list.refresh()
        self.parent.refresh(self.app.category)
        
        
    def draw(self):
        print self.size
        self.draw_background()
        self.draw_label()
        self.draw_icon()
        
    def draw_icon(self):
        try:
            self.image = Image( "../webmanager/media/%s" % str(self.app.icon) )
            x,y = list(self.center)
            self.image.pos = x - self.image.width /2, y - self.image.height /2      
            self.image.draw()
        except:
            #print "Icon Exception: Unrecognized type of format"
            pass
        
        
    def draw_background(self):
        style = {'bg-color': (1, 1, 1, 1), 'draw-background': 0, 'draw-border': True, 'border-radius': 10}
        set_color(*style.get('bg-color'))
        drawCSSRectangle(pos=self.pos, size=self.size,  style = style)


    def draw_label(self, dx=0, dy=0):
        pos = list(self.center)
        pos[1] -= 50
        drawLabel(label= self.label, pos=pos, size=(100,None), halign= 'center', anchor_y='top', font_size= 10)

