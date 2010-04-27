from pymt import *
from pymt.input.postproc.doubletap import InputPostprocDoubleTap
from popup import Popup
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
        kwargs.setdefault('size', (200,200))        
        
        self.double_tap_detected = False
        self.app = app
        self.pop = None
        super(AppButton, self).__init__(**kwargs)
        


    """Execute application on click"""
    def on_press( self, touch ):
        print 'on_press'
        self.double_tap_detected = touch.is_double_tap
        if self.double_tap_detected:
            self.open_app()
        #if single tap and popup not already open
        elif not self.pop:    
            print 'single tap and no popup'
            self.pop = Popup(self.app, pos= self.pos)
            self.time_delay(0.5, self.open_popup) #make sure is not a double tap
            

    def time_delay(self, time, function):
        self.timer = Timer(time, function).start()


    def open_popup(self):
        if self.double_tap_detected:
            return
        pop = self.pop    
        
        self.get_root_window().add_widget(self.pop)
        self.time_delay(5.0, self.close_popup) #retirar popup 
   
        
        
    def close_popup(self):
        print 'close popup'
        self.get_root_window().remove_widget(self.pop)
        self.pop = None
        
        
    def on_submit():
        self.open_app()
        
    
    def open_app(self):
        print '\nLoading %s...\n' % unicode(self.app)
        print 'ID: %i' % self.app.id
        print '\tPath: %s\n' % self.app.get_extraction_fullpath
        print '\tBoot file: %s\n' % self.app.get_boot_file()
        self.app.execute()

