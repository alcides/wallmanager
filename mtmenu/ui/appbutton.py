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
        kwargs.setdefault('size', (170,170))        
        
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
            self.pop = AppPopup(self.app, pos= self.pos)
            Timer(0.5, self.open_popup).start() #make sure is not a double tap



    def open_popup(self):
        if self.double_tap_detected:
            return  
        self.get_root_window().add_widget(self.pop)
        self.pop = None



    def open_app(self):
        print '\nLoading %s...\n' % unicode(self.app)
        print 'ID: %i' % self.app.id
        print '\tPath: %s\n' % self.app.get_extraction_fullpath
        print '\tBoot file: %s\n' % self.app.get_boot_file()
        self.app.execute()

