from pymt import *
from mtmenu.ui.apppopup import AppPopup
from threading import Timer
from config import APPSLIST_BTN_SIZE, APPSLIST_BTN_IMAGE_SIZE, APPSLIST_BTN_FONT_SIZE


class AppButton(MTKineticItem):
    """Widget representing an application on main window. 
    
    Arguments:
        app -- Application object attached to this widget
        kwargs -- Button properties, most of them inherited from MTButton
    
    This widget should be added to AppsGrid on Menu's UI construction"""
    def __init__(self, app, **kwargs):
        kwargs.setdefault('label', unicode(app))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('size', APPSLIST_BTN_SIZE)        
        
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
            self.pop = AppPopup(self.app, touch)
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
        from mtmenu import categories_list
        categories_list.refresh()
        self.parent.refresh(categories_list.current)
        
        
    def draw(self):
        
        # Outside line
        style = {'bg-color': (1, 1, 1, 1), 'draw-background': 0, 'draw-border': True, 'border-radius': 10}
        set_color(*style.get('bg-color'))
        drawCSSRectangle(pos=self.pos, size=self.size,  style = style)
        
        # Icon
        try:
            image = Image( "../webmanager/media/%s" % str(self.app.icon) )
            x,y = list(self.center)
            image.size = self.get_resized_size(image)
            image.pos = x - image.width /2, y - image.height /2      
            image.draw()
        except Exception as e:
            print "EXCEPTION on appbutton"
            print e
        
        # Label
        label_changed = False
        label_obj = MTLabel(label = self.label,
                            font_size = APPSLIST_BTN_FONT_SIZE,
                            autowidth = True)
        label_max_width = self.size[0] - 5
        
        while label_obj.width > label_max_width:

            self.label = self.label[:-1]
            
            label_changed = True
            label_obj = MTLabel(label = "%s..." % self.label,
                                pos = (self.pos[0] / 2, self.size[1]-50),
                                font_size = APPSLIST_BTN_FONT_SIZE,
                                autowidth = True)
            
        label_obj.pos = (self.pos[0] + ((self.size[0] - label_obj.width) / 2),
                         self.pos[1] - APPSLIST_BTN_FONT_SIZE - 6)
        
        if label_changed:
            self.label = "%s..." % self.label
            
        label_obj.draw()
    
    @staticmethod
    def get_resized_size (image):
        
        width, height = image.width, image.height
        max_width, max_height = list(APPSLIST_BTN_IMAGE_SIZE)
        
        # If width and height not higher than allowed, all good
        if width <= max_width and height <= max_height:
            return (width, height)
        
        # Scale maintaining aspect ratio
        scale = min(float(max_width) / width, 
                    float(max_height) / height)

        return (width * scale, height * scale)


